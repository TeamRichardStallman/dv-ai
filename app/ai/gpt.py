from openai import OpenAI
import json
from app.core.config import Config
from typing import List, Union

client_gpt = OpenAI(api_key=Config.OPENAI_API_KEY)


def generate_from_gpt(prompt: str, input: Union[dict, List]):
    user_content = json.dumps(input)
    response = client_gpt.chat.completions.create(
        model=Config.GPT_MODEL,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_content},
        ],
        response_format={"type": "json_object"},
        seed=Config.SEED,
        temperature=Config.TEMPERATURE,
        top_p=Config.TOP_P,
    )

    return json.loads(response.choices[0].message.content)
