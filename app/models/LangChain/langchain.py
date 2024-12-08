import json
from typing import Union

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langsmith import traceable

from app.core.config import Config
from app.schemas.evaluation import EvaluationRequestModel, PersonalEvaluationResponseModel, TechnicalEvaluationResponseModel
from app.schemas.question import QuestionsRequestModel, QuestionsResponseModel


class BaseGenerator:
    def __init__(self):
        self.llm = ChatOpenAI(
            api_key=Config.OPENAI_API_KEY, model=Config.GPT_MODEL, temperature=Config.TEMPERATURE, top_p=Config.TOP_P
        )

    def _clean_json(self, response_content: str) -> str:
        return response_content.strip().removeprefix("```json").removesuffix("```").strip()


class QuestionGenerator(BaseGenerator):
    @traceable
    def generate_questions(self, questions_prompt: str, additional_context: str) -> QuestionsResponseModel:
        chat_prompt = ChatPromptTemplate.from_messages([
            ("system", questions_prompt),
            ("human", additional_context)
        ])
        print(chat_prompt)

        chain = chat_prompt | self.llm
        response = chain.invoke({})
        response_content = response.content.strip()

        print(response_content)

        cleaned_content = self._clean_json(response_content)
        parsed_content = json.loads(cleaned_content)

        return QuestionsResponseModel(**parsed_content)


class EvaluationGenerator(BaseGenerator):
    def __init__(self, user_data: EvaluationRequestModel):
        super().__init__()
        self.user_data = user_data

    @traceable
    def evaluate(self, evaluation_prompt: str, qa_input: str) -> Union[TechnicalEvaluationResponseModel, PersonalEvaluationResponseModel]:
        chat_prompt = ChatPromptTemplate.from_messages([
            ("system", evaluation_prompt),
            ("human", "{qa_input}")
        ])
        print(chat_prompt)

        chain = chat_prompt | self.llm
        response = chain.invoke({"qa_input": qa_input})
        response_content = response.content.strip()

        print(response_content)

        cleaned_content = self._clean_json(response_content)
        parsed_content = json.loads(cleaned_content)

        if self.user_data.interview_type == "technical":
            return TechnicalEvaluationResponseModel(**parsed_content)
        else:
            return PersonalEvaluationResponseModel(**parsed_content)