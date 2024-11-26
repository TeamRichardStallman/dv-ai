import json
from datetime import datetime
from typing import Literal, Union

import weave
from openai import OpenAI

import wandb
from app.core.config import Config
from app.schemas.evaluation import EvaluationRequest, EvaluationResponse
from app.schemas.question import QuestionsRequest, QuestionsResponse

client_gpt = OpenAI(api_key=Config.OPENAI_API_KEY)

# W&B login
wandb.login(key=Config.WANDB_API_KEY)

weave.init("ticani0610-no/prompt-test")


class ContentGenerator(weave.Model):
    user_data: Union[QuestionsRequest, EvaluationRequest]

    @weave.op(call_display_name=lambda call: f"{call.func_name}__{datetime.now()}")
    def invoke(
        self, prompt: str, input: str, type: Literal["question", "evaluation"]
    ) -> Union[QuestionsResponse, EvaluationResponse]:
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

        if type == "question":
            weave.publish(weave.Dataset(name="dataset", rows=[{"cover_letter": input}]))
            return QuestionsResponse(**parsed_content)
        elif type == "evaluation":
            return EvaluationResponse(**parsed_content)
