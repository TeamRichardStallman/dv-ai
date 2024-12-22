import time
from operator import itemgetter
from typing import List, Literal, Union

from langchain.chains.query_constructor.base import AttributeInfo
from langchain.chains.summarize.chain import load_summarize_chain
from langchain.docstore.document import Document
from langchain.storage import InMemoryByteStore
from langchain.embeddings import CacheBackedEmbeddings
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import FlashrankRerank
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.retrievers.self_query.chroma import ChromaTranslator
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_chroma import Chroma
from langchain_core.output_parsers import PydanticOutputParser, CommaSeparatedListOutputParser, StrOutputParser
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
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

    def _build_query(self, keywords: List[str]) -> List[str]:
        """
        Builds multiple variations of a predefined technical question
        based on the provided keywords using an LLM.
        """
        try:
            # Predefined original question
            original_question = "What is the difference between an abstract class and an interface in Java?"

            # Define the reusable prompt template
            prompt_template = PromptTemplate(
                template="""
            You are an AI assistant specialized in generating technical interview questions. 
            Your task is to generate five different versions of the following technical question 
            by focusing on the related technical keywords provided.

            ORIGINAL QUESTION:
            {original_question}

            RELATED KEYWORDS:
            {keywords}

            Generate a list of alternative questions that are varied and focus on the technical aspects 
            of the keywords. Return them as a list separated by new lines.
            """
            )

            # Dynamically format the prompt with inputs
            prompt = prompt_template.format_prompt(
                original_question=original_question,
                keywords=", ".join(keywords),
            )

            return self.llm.invoke(prompt).content
        except Exception as e:
            # Graceful error handling
            print(f"Error in generating queries: {e}")
            return []

    def _extract_keywords(self, text: str) -> List[str]:
        """Extracts technical keywords using LLM."""
        output_parser = CommaSeparatedListOutputParser()
        prompt = PromptTemplate(
            template="""Extract the main technical skills and tools mentioned in the following cover letter:
            {cover_letter}
            
            Return them as a comma-separated list.
            """,
            input_variables=["cover_letter"],
            partial_variables={"format_instructions": output_parser.get_format_instructions()},
        )
        chain = prompt | self.llm | output_parser
        return chain.invoke(text)

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
        if self.request_data.interview_mode == "real" and self.request_data.interview_type == "technical":
            keywords = self._extract_keywords(text)
            print(f"Extracted Keywords: {keywords}")

            compressor = self._initialize_compressor()
            multi_queries = self._build_query(keywords)
            print("나오긴 함?", multi_queries)
            retriever = (
                ContextualCompressionRetriever(base_compressor=compressor, base_retriever=self.multiquery_retriever)
                if compressor
                else self.multiquery_retriever
            )

            docs = retriever.invoke(multi_queries)
            return "\n\n".join([doc.page_content for doc in docs])

        return ""

    @traceable
    def generate_questions(
        self, questions_prompt: PromptTemplate, additional_context: str, interview_id: int
    ) -> QuestionsResponseModel:
        """Generates interview questions based on prompts and context."""
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
