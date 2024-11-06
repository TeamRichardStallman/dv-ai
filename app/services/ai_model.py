import json
from app.ai.gpt import generate_from_gpt
from app.prompts.question import generate_questions_prompt
from app.prompts.evaluation import generate_evaluation_prompt
from app.utils.generate import generate_file_objects, generate_file_data
from app.models.questions_response import QusetionsRequest
from app.models.evaluation_response import EvaluationRequest
from app.utils.merge import merge_questions_and_answers


async def generate_questions(user_data: QusetionsRequest):
    prompt = generate_questions_prompt(user_data)

    file_objects = generate_file_objects(user_data.file_paths)
    file_data = await generate_file_data(file_objects)

    cover_letter = ""
    if file_data and "data" in file_data[0] and "data" in file_data[0]["data"]:
        cover_letter = file_data[0]["data"]["data"]

    data = generate_from_gpt(prompt, cover_letter, "question")
    return data


def evaluate_interview(user_data: EvaluationRequest):
    merged_input = merge_questions_and_answers(user_data.questions, user_data.answers)
    merged_input_str = json.dumps(merged_input)

    prompt = generate_evaluation_prompt(user_data)
    data = generate_from_gpt(prompt, merged_input_str, "evaluation")
    return data
