import json
import os

import weave
from dotenv import load_dotenv
from openai import OpenAI

from app.models.openai.gpt import ContentGenerator
from app.schemas.evaluation import EvaluationRequest
from app.schemas.question import QuestionsRequest
from app.services.evaluation_service import generate_evaluation_prompt
from app.services.question_service import generate_questions_prompt
from app.utils.generate import generate_file_data, generate_file_objects
from app.utils.merge import merge_questions_and_answers

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client_gpt = OpenAI(api_key=OPENAI_API_KEY)

weave.init("ticani0610-no/prompt-test")


async def generate_questions(user_data: QuestionsRequest):
    prompt = generate_questions_prompt(user_data)

    file_objects = generate_file_objects(user_data.file_paths)
    file_data = await generate_file_data(file_objects)

    cover_letter = ""
    cover_letter_data = next((item for item in file_data if item["type"] == "cover-letter"), None)

    if cover_letter_data and "data" in cover_letter_data and "data" in cover_letter_data["data"]:
        cover_letter = cover_letter_data["data"]["data"]
    else:
        print("Cover letter data not found or missing required fields:", cover_letter_data)

    generator = ContentGenerator(user_data=user_data)
    data = generator.invoke(prompt, cover_letter, "question")
    return data


def evaluate_interview(user_data: EvaluationRequest):
    merged_input = merge_questions_and_answers(user_data.questions, user_data.answers)
    merged_input_str = json.dumps(merged_input, ensure_ascii=False)

    prompt = generate_evaluation_prompt(user_data)

    generator = ContentGenerator(user_data=user_data)
    data = generator.invoke(prompt, merged_input_str, "evaluation")

    return data
