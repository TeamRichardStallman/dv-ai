import time
from operator import itemgetter
from typing import List, Literal, Union

from langchain.chains.query_constructor.base import AttributeInfo
from langchain.chains.summarize.chain import load_summarize_chain
from langchain.docstore.document import Document
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import FlashrankRerank
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.retrievers.self_query.chroma import ChromaTranslator
from langchain_chroma import Chroma
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
)
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

vectorstore = Chroma(
    persist_directory="app/chroma_vectorDB", embedding_function=OpenAIEmbeddings(), collection_name="my_db"
)


# 메타데이터 필드 정보 생성
metadata_field_info = [
    AttributeInfo(
        name="Category",
        description=(
            "The high-level classification or domain that the content belongs to. "
            "Example include comprehensive lists, database technologies, programming languages, "
            "frameworks, platforms, caching technologies, design patterns, networks, data science, "
            "blockchain, security, DevOps, data structures, operating systems (OS), coding exercises, algorithms]."
        ),
        type="string",
    ),
    AttributeInfo(
        name="Technology",
        description=(
            "The specific technology, language, framework, tool, or platform referenced in the content. "
            "Examples include JavaScript, Python, Android, Docker, ReactJS, SQL, Ruby, Swift, Angular, "
            "MongoDB, Redis, Golang, C++, NodeJS, C#, iOS, Spark, and more."
        ),
        type="string",
    ),
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
    """Generates questions based on a cover letter and job role."""

    def _extract_keywords_with_llm(self, text: str) -> List[str]:
        """Extracts technical keywords using LLM."""
        prompt = PromptTemplate(
            template="Extract all technical terms, programming languages, frameworks, tools, and technologies mentioned in the following cover letter. Only list the terms, separated by commas.\n\nCover Letter:\n{cover_letter}",
            input_variables=["cover_letter"],
        )
        try:
            response = self.llm.invoke(prompt.format(cover_letter=text))
            keywords = [keyword.strip() for keyword in response.content.split(",") if keyword.strip()]
            return keywords
        except Exception as e:
            print(f"Error extracting keywords: {e}")
            return []

    def _initialize_retriever(self, keywords: List[str]) -> ContextualCompressionRetriever:
        """Initializes the retriever with metadata filtering and compression."""

        def retry_compressor(max_retries=5, delay=2):
            """Retries initializing FlashrankRerank up to max_retries times."""
            attempt = 0
            while attempt < max_retries:
                try:
                    print(f"Attempt {attempt + 1}/{max_retries} to initialize FlashrankRerank...")
                    return FlashrankRerank(model="ms-marco-MultiBERT-L-12")
                except Exception as e:
                    print(f"Error on attempt {attempt + 1}: {e}")
                    attempt += 1
                    time.sleep(delay)
            print("Failed to initialize FlashrankRerank after multiple retries. Using fallback compressor.")
            return None

        retriever = SelfQueryRetriever.from_llm(
            llm=self.llm,
            vectorstore=vectorstore,
            document_contents="Brief summary of a Technical Question",
            metadata_field_info=metadata_field_info,
            structured_query_translator=ChromaTranslator(),
            search_type="mmr",
            search_kwargs={
                "k": 5,
                "filter": {"$or": [{"Technology": {"$in": keywords}}, {"Category": {"$in": keywords}}]},
            },
        )

        compressor = retry_compressor()

        # If compressor fails, return retriever without compression
        if compressor is None:
            return retriever

        # Return retriever with compression if successful
        return ContextualCompressionRetriever(base_compressor=compressor, base_retriever=retriever)

    def _generate_reference(self, text: str) -> str:
        """Generates reference data by summarizing text and retrieving related documents if conditions are met."""
        if self.request_data.interview_mode == "real" and self.request_data.interview_type == "technical":
            # 기술 키워드 추출
            extracted_keywords = self._extract_keywords_with_llm(text)
            print(f"Extracted Keywords: {extracted_keywords}")

            # 문서 요약
            summary_chain = load_summarize_chain(self.llm, chain_type="map_reduce")
            summary = summary_chain.invoke([Document(page_content=text)]).get("output_text")

            # Retriever 초기화 및 검색
            compression_retriever = self._initialize_retriever(extracted_keywords)
            retrieved_docs = compression_retriever.invoke(summary)
            return "\n\n".join([doc.page_content for doc in retrieved_docs])

        # RAG 조건을 만족하지 않으면 빈 문자열 반환
        return ""

    @traceable
    def generate_questions(
        self, questions_prompt: PromptTemplate, additional_context: str, interview_id: int
    ) -> QuestionsResponseModel:
        """Generates interview questions based on prompts and context."""
        chat_prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template(questions_prompt.template),
                HumanMessagePromptTemplate.from_template(additional_context),
            ]
        )

        parser = PydanticOutputParser(pydantic_object=QuestionsResponseModel)

        # 체인 생성
        chain = (
            {
                "job_role": itemgetter("job_role"),
                "question_count": itemgetter("question_count"),
                "user_id": itemgetter("user_id"),
                "interview_id": itemgetter("interview_id"),
                "cover_letter": itemgetter("cover_letter"),
                "reference": itemgetter("cover_letter") | RunnableLambda(self._generate_reference),
            }
            | chat_prompt
            | self.llm
            | parser
        )

        # 체인 실행
        response = chain.invoke(
            {
                "job_role": self.request_data.job_role,
                "question_count": self.request_data.question_count,
                "user_id": self.request_data.user_id,
                "interview_id": interview_id,
                "cover_letter": additional_context,
            }
        )

        return response


class EvaluationGenerator(BaseGenerator):
    @traceable
    def evaluate(
        self,
        evaluation_prompt: str,
        qa_input: str,
        choice: Literal["answer", "evaluation"],
    ) -> Union[
        TechnicalAnswerResponseModel,
        PersonalAnswerResponseModel,
        TechnicalEvaluationResponseModel,
        PersonalEvaluationResponseModel,
    ]:
        parser = self._get_parser(choice)

        chat_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", evaluation_prompt),
                ("human", "{qa_input}"),
            ]
        )

        chain = chat_prompt | self.llm | parser

        return chain.invoke({"qa_input": qa_input})

    def _get_parser(self, choice: Literal["answer", "evaluation"]):
        if choice == "answer":
            if self.request_data.interview_type == "technical":
                return PydanticOutputParser(pydantic_object=TechnicalAnswerResponseModel)
            elif self.request_data.interview_type == "personal":
                return PydanticOutputParser(pydantic_object=PersonalAnswerResponseModel)
            else:
                raise ValueError(f"Invalid interview type: {self.request_data.interview_type}")
        elif choice == "evaluation":
            if self.request_data.interview_type == "technical":
                return PydanticOutputParser(pydantic_object=TechnicalEvaluationResponseModel)
            elif self.request_data.interview_type == "personal":
                return PydanticOutputParser(pydantic_object=PersonalEvaluationResponseModel)
            else:
                raise ValueError(f"Invalid interview type: {self.request_data.interview_type}")
