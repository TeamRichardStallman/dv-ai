import json
from datetime import datetime
from typing import Any, Literal, Union

import weave
from openai import OpenAI

import wandb
from app.config import Config
from app.models.evaluation_response import EvaluationRequest
from app.models.questions_response import QuestionsRequest

client_gpt = OpenAI(api_key=Config.OPENAI_API_KEY)

# W&B login
wandb.login(key=Config.WANDB_API_KEY)

weave.init("ticani0610-no/prompt-test")


class ContentGenerator(weave.Model):
    user_data: Union[dict, QuestionsRequest, EvaluationRequest]

    @weave.op(call_display_name=lambda call: f"{call.func_name}__{datetime.now()}")
    def invoke(self, prompt: str, input: str, type: Literal["question", "evaluation"]) -> Any:
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

        if type == "question":
            weave.publish(weave.Dataset(name="dataset", rows=[{"cover_letter": input}]))
        response_content = response.choices[0].message.content
        return json.loads(response_content)
