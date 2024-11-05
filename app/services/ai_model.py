import json
from app.ai.gpt import ContentGenerator
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
    cover_letter_data = next((item for item in file_data if item["type"] == "cover-letter"), None)

    if cover_letter_data and "data" in cover_letter_data and "data" in cover_letter_data["data"]:
        cover_letter = cover_letter_data["data"]["data"]
    else:
        print("Cover letter data not found or missing required fields:", cover_letter_data)

    generator = ContentGenerator()
    data = generator.invoke(prompt, cover_letter, "question")
    return data


def evaluate_interview(user_data: EvaluationRequest):
    merged_input = merge_questions_and_answers(user_data.questions, user_data.answers)
    # merged_input_str = json.dumps(merged_input)

    prompt = generate_evaluation_prompt(user_data)
    generator = ContentGenerator()
    data = generator.invoke(prompt, merged_input, "evaluation")
    return data
