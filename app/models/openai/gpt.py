import json
from typing import Literal, Union

from openai import OpenAI

from app.core.config import Config
from app.schemas.evaluation import (
    EvaluationRequestModel,
    PersonalEvaluationResponseModel,
    TechnicalEvaluationResponseModel,
)
from app.schemas.question import QuestionsRequestModel, QuestionsResponseModel

client_gpt = OpenAI(api_key=Config.OPENAI_API_KEY)


class ContentGenerator:
    def __init__(self, user_data: Union[QuestionsRequestModel, EvaluationRequestModel]):
        self.user_data = user_data

    def invoke(self, prompt: str, input: str, choice: Literal["question", "evaluation"]):
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

        response_content = response.choices[0].message.content
        parsed_content = json.loads(response_content)

        if choice == "question":
            return QuestionsResponseModel(**parsed_content)
        elif choice == "evaluation":
            if self.user_data.interview_type == "technical":
                return TechnicalEvaluationResponseModel(**parsed_content)
            elif self.user_data.interview_type == "personal":
                return PersonalEvaluationResponseModel(**parsed_content)
