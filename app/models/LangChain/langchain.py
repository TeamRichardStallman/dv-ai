import json
from typing import Literal, Union

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langsmith import traceable

from app.core.config import Config
from app.schemas.evaluation import EvaluationRequest, PersonalEvaluationResponse, TechnicalEvaluationResponse
from app.schemas.question import QuestionsRequest, QuestionsResponse


class ContentGenerator:
    def __init__(self, user_data: Union[QuestionsRequest, EvaluationRequest]):
        self.user_data = user_data
        self.llm = ChatOpenAI(
            api_key=Config.OPENAI_API_KEY, model=Config.GPT_MODEL, temperature=Config.TEMPERATURE, top_p=Config.TOP_P
        )

    @traceable
    def invoke(
        self, prompt: str, input: str, choice: Literal["question", "evaluation"]
    ) -> Union[QuestionsResponse, TechnicalEvaluationResponse, PersonalEvaluationResponse]:
        messages = [SystemMessage(content=prompt), HumanMessage(content=input)]

        # Generate response using the LLM
        response = self.llm.invoke(messages)
        response_content = response.content
        print(response_content)

        # Remove response using the LLM
        if response_content.startswith("```json"):
            response_content = response_content[len("```json") :]

        if response_content.endswith("```"):
            response_content = response_content[: -len("```")]

        # Strip leading/trailing whitespace
        response_content = response_content.strip()
        parsed_content = json.loads(response_content)

        # Return the appropriate response object
        if choice == "question":
            return QuestionsResponse(**parsed_content)
        elif choice == "evaluation":
            if self.user_data.interview_type == "technical":
                return TechnicalEvaluationResponse(**parsed_content)
            elif self.user_data.interview_type == "personal":
                return PersonalEvaluationResponse(**parsed_content)
