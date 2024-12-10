from typing import Union, Literal

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from langsmith import traceable

from app.core.config import Config
from app.schemas.answer import AnswerResponseModel
from app.schemas.evaluation import (
    EvaluationRequestModel,
    PersonalEvaluationResponseModel,
    TechnicalEvaluationResponseModel,
)
from app.schemas.question import QuestionsRequestModel, QuestionsResponseModel


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
    @traceable
    def generate_questions(self, questions_prompt: str, additional_context: str) -> QuestionsResponseModel:
        chat_prompt = ChatPromptTemplate.from_messages([
            ("system", questions_prompt),
            ("human", additional_context),
        ])

        parser = PydanticOutputParser(pydantic_object=QuestionsResponseModel)

        chain = chat_prompt | self.llm | parser
        return chain.invoke({})


class EvaluationGenerator(BaseGenerator):
    @traceable
    def evaluate(
        self,
        evaluation_prompt: str,
        qa_input: str,
        choice: Literal["answer", "evaluation"],
    ) -> Union[TechnicalEvaluationResponseModel, PersonalEvaluationResponseModel, AnswerResponseModel]:
        parser = self._get_parser(choice)

        chat_prompt = ChatPromptTemplate.from_messages([
            ("system", evaluation_prompt),
            ("human", "{qa_input}"),
        ])

        chain = chat_prompt | self.llm | parser
        return chain.invoke({"qa_input": qa_input})

    def _get_parser(self, choice: Literal["answer", "evaluation"]):
        if choice == "answer":
            return PydanticOutputParser(pydantic_object=AnswerResponseModel)
        elif choice == "evaluation":
            if self.request_data.interview_type == "technical":
                return PydanticOutputParser(pydantic_object=TechnicalEvaluationResponseModel)
            elif self.request_data.interview_type == "personal":
                return PydanticOutputParser(pydantic_object=PersonalEvaluationResponseModel)
            else:
                raise ValueError(f"Invalid interview type: {self.request_data.interview_type}")