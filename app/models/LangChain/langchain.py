import logging
import time
from operator import itemgetter
from typing import List, Literal, Union

from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.chains.query_constructor.base import AttributeInfo
from langchain.embeddings import CacheBackedEmbeddings
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import FlashrankRerank
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.storage import InMemoryByteStore
from langchain.tools.retriever import create_retriever_tool
from langchain_chroma import Chroma
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.output_parsers import CommaSeparatedListOutputParser, PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langsmith import traceable

from app.core.config import Config
from app.schemas.answer import PersonalAnswerResponseModel, TechnicalAnswerResponseModel
from app.schemas.evaluation import (
    EvaluationRequestModel,
    PersonalEvaluationResponseModel,
    TechnicalEvaluationResponseModel,
)
from app.schemas.question import QuestionsRequestModel, QuestionsResponseModel


# Preloading reusable resources
class ResourceLoader:
    embedding_model = "text-embedding-3-small"

    @staticmethod
    def get_cached_embedder():
        embedding = OpenAIEmbeddings(model=ResourceLoader.embedding_model)
        store = InMemoryByteStore()
        return CacheBackedEmbeddings.from_bytes_store(embedding, store, namespace=embedding.model)

    @staticmethod
    def get_vectorstore():
        cached_embedder = ResourceLoader.get_cached_embedder()
        return Chroma(
            persist_directory="app/question_DB",
            embedding_function=cached_embedder,
            collection_name="my_db",
        )

    @staticmethod
    def get_metadata_field_info():
        return [
            AttributeInfo(
                name="category",
                description="The category or topic related to the question, e.g., 'jQuery', 'Redis', 'Spark'.",
                type="string",
            )
        ]


class BaseGenerator:
    def __init__(self, request_data: Union[QuestionsRequestModel, EvaluationRequestModel]):
        self.request_data = request_data
        self.llm = ChatOpenAI(
            api_key=Config.OPENAI_API_KEY,
            model=Config.GPT_MODEL,
            temperature=Config.TEMPERATURE,
            top_p=Config.TOP_P,
        )


class QuestionGenerator(BaseGenerator):
    """Generates interview questions based on cover letter and job role."""

    def __init__(self, request_data: QuestionsRequestModel):
        super().__init__(request_data)
        self.retriever = SelfQueryRetriever.from_llm(
            llm=self.llm,
            vectorstore=ResourceLoader.get_vectorstore(),
            document_contents="A question about a technical topic with its category.",
            metadata_field_info=ResourceLoader.get_metadata_field_info(),
        )
        self.multiquery_retriever = MultiQueryRetriever.from_llm(llm=self.llm, retriever=self.retriever)
        self.query_cache = {}  # Initialize cache

    def _log(self, message: str):
        """Log a message for debugging."""
        logger = logging.getLogger(__name__)
        logger.info(message)

    def _generate_reference(self, text: str) -> str:
        """Generates summarized reference data and retrieves related documents."""
        try:
            if self.request_data.interview_mode != "real" or self.request_data.interview_type != "technical":
                return ""

            keywords = self._extract_keywords(text)
            self._log(f"Extracted Keywords: {keywords}")

            # Use keywords as a cache key
            cache_key = tuple(sorted(keywords))
            if cache_key in self.query_cache:
                self._log("Using cached results")
                return self.query_cache[cache_key]

            queries = [f'"{keyword}"' for keyword in keywords]
            batch_inputs = [{"input": query} for query in queries]

            # Initialize compressor
            compressor = self._initialize_compressor()
            retriever = (
                ContextualCompressionRetriever(base_compressor=compressor, base_retriever=self.retriever)
                if compressor
                else self.multiquery_retriever
            )

            tools = [
                TavilySearchResults(k=6),
                create_retriever_tool(
                    retriever,
                    name="question_search",
                    description="Use this tool to extract questions where the metadata key 'category' matches any of the given keywords, focusing on retrieving relevant technical questions.",
                ),
            ]

            prompt = ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        "You are a helpful assistant. Use the `question_search` tool to find relevant questions "
                        "matching the metadata key 'category' and given keywords. If you cannot find suitable information using `question_search`, switch to "
                        "the `search` tool to perform a broader web search.",
                    ),
                    ("human", "{input}"),
                    ("placeholder", "{agent_scratchpad}"),
                ]
            )

            agent = create_tool_calling_agent(self.llm, tools, prompt)
            agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False)

            # Execute query in batch
            responses = agent_executor.batch(batch_inputs, return_only_outputs=True)

            outputs = [response["output"] for response in responses if "output" in response]

            # Cache the results
            combined_results = "\n\n".join(outputs)
            self.query_cache[cache_key] = combined_results
            return combined_results
        except Exception as e:
            self._log(f"Error in generating reference: {e}")
            return "Error occurred while generating reference data."

    def _extract_keywords(self, text: str) -> List[str]:
        """Extracts technical keywords using LLM."""
        try:
            output_parser = CommaSeparatedListOutputParser()
            prompt_template = PromptTemplate(
                template="""
                You are an expert in identifying technical skills and tools.
                Extract the 3 most relevant technical skills and tools mentioned in the following text, focusing specifically on the job role: {job_role}.

                TEXT:
                {cover_letter}

                Return them as a comma-separated list.
                """,
                input_variables=["cover_letter", "job_role"],
                partial_variables={"format_instructions": output_parser.get_format_instructions()},
            )
            chain = prompt_template | self.llm | output_parser
            return chain.invoke({"cover_letter": text, "job_role": self.request_data.job_role})
        except Exception as e:
            self._log(f"Error in extracting keywords: {e}")
            return ["Java", "Python", "Redis"]  # Fallback default keywords

    def _initialize_compressor(self, max_retries=5, delay=2):
        """Initializes a document compressor with retry logic."""
        for attempt in range(max_retries):
            try:
                self._log(f"Attempt {attempt + 1}/{max_retries} to initialize FlashrankRerank...")
                return FlashrankRerank(model="ms-marco-MultiBERT-L-12")
            except Exception as e:
                self._log(f"Error on attempt {attempt + 1}: {e}")
                time.sleep(delay)
        self._log("Failed to initialize FlashrankRerank. Proceeding without compression.")
        return None

    @traceable
    def generate_questions(
        self, questions_prompt: PromptTemplate, additional_context: str, interview_id: int
    ) -> QuestionsResponseModel:
        """Generates interview questions based on prompts and context."""
        try:
            parser = PydanticOutputParser(pydantic_object=QuestionsResponseModel)

            # Prepare dynamic prompt
            prepared_prompt = questions_prompt.partial(
                job_role=self.request_data.job_role,
                question_count=self.request_data.question_count,
                user_id=self.request_data.user_id,
                interview_id=interview_id,
            )

            # Create and execute chain
            chain = (
                {
                    "cover_letter": itemgetter("cover_letter"),
                    "reference": itemgetter("cover_letter") | RunnableLambda(self._generate_reference),
                }
                | prepared_prompt
                | self.llm
                | parser
            )
            return chain.invoke({"cover_letter": additional_context})
        except Exception as e:
            self._log(f"Error in generating questions: {e}")
            raise RuntimeError("Failed to generate questions.") from e


class EvaluationGenerator(BaseGenerator):
    @traceable
    def evaluate(
        self,
        evaluation_prompt: PromptTemplate,
        qa_input: str,
        interview_id: int,
        choice: Literal["answer", "evaluation"],
        wpm: float = 0.0,
    ) -> Union[
        TechnicalAnswerResponseModel,
        PersonalAnswerResponseModel,
        TechnicalEvaluationResponseModel,
        PersonalEvaluationResponseModel,
    ]:
        parser = self._get_parser(choice)

        chat_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", evaluation_prompt.template),
                ("human", "{qa_input}"),
            ]
        )

        chain = chat_prompt | self.llm | parser

        # Base input for both request types
        input_data = {
            "job_role": self.request_data.job_role,
            "interview_type": self.request_data.interview_type,
            "user_id": self.request_data.user_id,
            "interview_id": interview_id,
            "wpm": wpm,
            "qa_input": qa_input,
        }

        if hasattr(self.request_data, "answer"):
            input_data.update(
                {
                    "question_id": getattr(self.request_data, "question", {}).get("question_id", None),
                    "s3_audio_url": getattr(self.request_data.answers, "s3_audio_url", None),
                    "s3_video_url": getattr(self.request_data.answers, "s3_video_url", None),
                }
            )

        return chain.invoke(input_data)

    def _get_parser(self, choice: Literal["answer", "evaluation"]):
        parsers = {
            "answer": {
                "technical": TechnicalAnswerResponseModel,
                "personal": PersonalAnswerResponseModel,
            },
            "evaluation": {
                "technical": TechnicalEvaluationResponseModel,
                "personal": PersonalEvaluationResponseModel,
            },
        }

        # Fetch the appropriate parser model
        model = parsers.get(choice, {}).get(self.request_data.interview_type)
        if not model:
            raise ValueError(
                f"Invalid combination of choice '{choice}' and interview type '{self.request_data.interview_type}'"
            )

        return PydanticOutputParser(pydantic_object=model)
