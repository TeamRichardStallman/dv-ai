import json
from typing import Literal, Union

from openai import OpenAI

from app.core.config import Config
from app.schemas.answer import AnswerResponseModel
from app.schemas.evaluation import (
    EvaluationRequestModel,
    PersonalEvaluationResponseModel,
    TechnicalEvaluationResponseModel,
)
from app.schemas.question import QuestionsRequestModel, QuestionsResponseModel
from app.utils.generate import ensure_feedback_fields

client_gpt = OpenAI(api_key=Config.OPENAI_API_KEY)


class ContentGenerator:
    def __init__(self, request_data: Union[QuestionsRequestModel, EvaluationRequestModel]):
        self.request_data = request_data

    def invoke(self, prompt: str, input: str, choice: Literal["question", "answer", "evaluation"]):
        response = client_gpt.chat.completions.create(
            model=Config.GPT_MODEL,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": input},
            ],
            response_format={"type": "json_object"},
            seed=Config.SEED,
            temperature=Config.TEMPERATURE,
            top_p=Config.TOP_P,
        )
        try:
            response_content = response.choices[0].message.content
            parsed_content = json.loads(response_content)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON response from GPT: {e}")

        if choice == "question":
            return QuestionsResponseModel(**parsed_content)
        elif choice == "answer":
            parsed_content = ensure_feedback_fields(parsed_content)
            return AnswerResponseModel(**parsed_content)
        elif choice == "evaluation":
            if self.request_data.interview_type == "technical":
                return TechnicalEvaluationResponseModel(**parsed_content)
            elif self.request_data.interview_type == "personal":
                return PersonalEvaluationResponseModel(**parsed_content)
