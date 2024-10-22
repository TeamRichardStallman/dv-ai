from app.utils.llm_config import GPT_MODEL, SEED, TEMPERATURE, TOP_P
from app.utils.prompts import generate_questions_prompt
from openai import OpenAI
import json
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client_gpt = OpenAI(api_key = OPENAI_API_KEY)

def generate_questions_from_cover_letter(cover_letter: str, user_data: dict):
    prompt = generate_questions_prompt(user_data)
    
    response = client_gpt.chat.completions.create(
        model=GPT_MODEL,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": cover_letter}
        ],
        response_format={"type": "json_object"},
        seed=SEED,
        temperature=TEMPERATURE,
        top_p=TOP_P
    )
    
    return json.loads(response.choices[0].message.content)["questions"]