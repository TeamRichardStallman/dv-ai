import time
import os
from operator import itemgetter
from typing import List, Literal, Union, Dict

from langchain.chains.query_constructor.base import AttributeInfo
from langchain.storage import InMemoryByteStore
from langchain.embeddings import CacheBackedEmbeddings
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import FlashrankRerank
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_chroma import Chroma
from langchain_core.output_parsers import PydanticOutputParser, CommaSeparatedListOutputParser
from langchain_core.prompts import (
    ChatPromptTemplate,
    PromptTemplate,
)
from langchain_core.runnables import RunnableLambda
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.tools.retriever import create_retriever_tool
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langsmith import traceable

from app.core.config import Config
from app.schemas.answer import PersonalAnswerResponseModel, TechnicalAnswerResponseModel
from app.schemas.evaluation import (
    EvaluationRequestModel,
    PersonalEvaluationResponseModel,
    TechnicalEvaluationResponseModel,
)
from app.schemas.question import QuestionsRequestModel, QuestionsResponseModel

os.environ["TAVILY_API_KEY"] = "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"


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

    def _build_query(self, keywords: List[str]) -> List[str]:
        """
        Builds multiple variations of a predefined technical question
        based on the provided keywords using an LLM.
        """
        try:
            original_question = "What is the difference between an abstract class and an interface in Java?"
            prompt_template = PromptTemplate(
                template="""
                You are an AI assistant specialized in generating technical interview questions. 
                Generate five different versions of the following technical question, focusing on 
                the related technical keywords provided.

                ORIGINAL QUESTION:
                {original_question}

                RELATED KEYWORDS:
                {keywords}

                Return a list of alternative questions separated by new lines.
                """
            )
            prompt = prompt_template.format_prompt(
                original_question=original_question,
                keywords=", ".join(keywords),
            )
            response = self.llm.invoke(prompt).content
            return [query.strip() for query in response.split("\n") if query.strip()]
        except Exception as e:
            print(f"Error in generating queries: {e}")
            return self._fallback_questions(keywords)

    @staticmethod
    def _fallback_questions(keywords: List[str]) -> List[str]:
        """Provides default questions in case of an error."""
        return [
            (
                f"What are the key differences between {keywords[0]} and {keywords[1]}?"
                if len(keywords) > 1
                else "What is the role of this concept in software development?"
            ),
            "Can you explain the advantages of using this technique?",
            "What are the common use cases for this approach?",
        ]

    def _extract_keywords(self, text: str) -> List[str]:
        """Extracts technical keywords using LLM."""
        try:
            output_parser = CommaSeparatedListOutputParser()
            prompt_template = PromptTemplate(
                template="""
                Extract the main technical skills and tools mentioned in the following text:
                {cover_letter}

                Return them as a comma-separated list.
                """,
                input_variables=["cover_letter"],
                partial_variables={"format_instructions": output_parser.get_format_instructions()},
            )
            chain = prompt_template | self.llm | output_parser
            return chain.invoke(text)
        except Exception as e:
            print(f"Error in extracting keywords: {e}")
            return ["Java", "Python", "Redis", "MongoDB", "AWS"]

    def _initialize_compressor(self, max_retries=5, delay=2):
        """Initializes a document compressor with retry logic."""
        for attempt in range(max_retries):
            try:
                print(f"Attempt {attempt + 1}/{max_retries} to initialize FlashrankRerank...")
                return FlashrankRerank(model="ms-marco-MultiBERT-L-12")
            except Exception as e:
                print(f"Error on attempt {attempt + 1}: {e}")
                time.sleep(delay)
        print("Failed to initialize FlashrankRerank. Proceeding without compression.")
        return None

    def _generate_reference(self, text: str) -> str:
        """Generates summarized reference data and retrieves related documents."""
        try:
            if self.request_data.interview_mode == "real" and self.request_data.interview_type == "technical":
                keywords = self._extract_keywords(text)
                print(f"Extracted Keywords: {keywords}")

                compressor = self._initialize_compressor()
                multi_queries = self._build_query(keywords)

                retriever = (
                    ContextualCompressionRetriever(base_compressor=compressor, base_retriever=self.multiquery_retriever)
                    if compressor
                    else self.multiquery_retriever
                )

                tools = [
                    TavilySearchResults(k=6),
                    create_retriever_tool(
                        retriever,
                        name="question_search",
                        description="Use this tool to search relevant questions from the question document.",
                    ),
                ]

                prompt = ChatPromptTemplate.from_messages(
                    [
                        (
                            "system",
                            "You are a helpful assistant. Your primary task is to use the `question_search` tool to find relevant questions "
                            "from the question document. If you cannot find suitable information using `question_search`, then switch to "
                            "the `search` tool to perform a broader web search. Always ensure that your responses are based on the most relevant information "
                            "retrieved from these tools.",
                        ),
                        ("human", "{input}"),
                        ("placeholder", "{agent_scratchpad}"),
                    ]
                )

                agent = create_tool_calling_agent(self.llm, tools, prompt)
                agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False)
                docs: Dict = agent_executor.invoke({"input": multi_queries})
                return docs
            return ""
        except Exception as e:
            print(f"Error in generating reference: {e}")
            return "Error occurred while generating reference data."

    @traceable
    def generate_questions(
        self, questions_prompt: PromptTemplate, additional_context: str, interview_id: int
    ) -> QuestionsResponseModel:
        """Generates interview questions based on prompts and context."""
        try:
            parser = PydanticOutputParser(pydantic_object=QuestionsResponseModel)

            prepared_prompt = questions_prompt.partial(
                job_role=self.request_data.job_role,
                question_count=self.request_data.question_count,
                user_id=self.request_data.user_id,
                interview_id=interview_id,
            )

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
            print(f"Error in generating questions: {e}")
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
