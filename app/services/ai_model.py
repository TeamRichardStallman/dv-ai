from app.ai.gpt import generate_from_gpt
from app.prompts.question import generate_questions_prompt
from app.prompts.evaluation import generate_evaluation_prompt
from app.utils.save_file import save_prompt_and_result
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client_gpt = OpenAI(api_key=OPENAI_API_KEY)


def generate_questions(cover_letter: str, user_data: dict):
    prompt = generate_questions_prompt(user_data)
    data = generate_from_gpt(prompt, cover_letter, "question")
    save_prompt_and_result(prompt, cover_letter, data)
    return data


def evaluate_interview(merged_input: str, user_data: dict):
    prompt = generate_evaluation_prompt(user_data)
    data = generate_from_gpt(prompt, merged_input, "evaluation")
    save_prompt_and_result(prompt, merged_input, data)
    return data
