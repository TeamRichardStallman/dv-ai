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
from app.services.s3_service import S3Service
from app.utils.generate import create_file_objects, get_cover_letters_data
from app.utils.merge import merge_questions_and_answers

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client_gpt = OpenAI(api_key=OPENAI_API_KEY)

weave.init("ticani0610-no/prompt-test")


async def generate_interview_questions(user_data: QuestionsRequest):
    s3_service = S3Service()
    prompt = generate_questions_prompt(user_data)

    file_objects = create_file_objects(user_data.file_paths)
    file_data = await s3_service.get_files_from_s3(file_objects)
    cover_letter = get_cover_letters_data(file_data)
    cover_letter = cover_letter or ""

    generator = ContentGenerator(user_data=user_data)
    data = generator.invoke(prompt, cover_letter, "question")
    return data


def generate_interview_evaluation(user_data: EvaluationRequest):
    prompt = generate_evaluation_prompt(user_data)

    merged_input = merge_questions_and_answers(user_data.questions, user_data.answers)
    merged_input_str = json.dumps(merged_input, ensure_ascii=False)

    generator = ContentGenerator(user_data=user_data)
    data = generator.invoke(prompt, merged_input_str, "evaluation")
    return data
