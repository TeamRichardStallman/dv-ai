import json
import logging
import os
from typing import Union

import weave
from dotenv import load_dotenv
from openai import OpenAI

from app.models.openai.gpt import ContentGenerator
from app.schemas.answer import AnswerRequestModel, AnswerResponseModel
from app.schemas.evaluation import (
    EvaluationRequestModel,
    PersonalEvaluationResponseModel,
    TechnicalEvaluationResponseModel,
)
from app.schemas.question import QuestionsRequestModel, QuestionsResponseModel
from app.services.answer_service import generate_answer_evaluation_new_request_data, generate_answer_evaluation_prompt
from app.services.evaluation_service import generate_interview_evaluation_prompt
from app.services.question_service import generate_questions_prompt
from app.services.s3_service import S3Service, get_s3_service
from app.services.stt_service import get_stt_service
from app.services.tts_service import get_tts_service
from app.utils.generate import create_file_objects, get_cover_letters_data
from app.utils.merge import merge_question_and_answer, merge_questions_and_answers

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client_gpt = OpenAI(api_key=OPENAI_API_KEY)

weave.init("ticani0610-no/prompt-test")

logging.basicConfig(level=logging.INFO)


async def process_interview_questions(
    interview_id: Union[int, str],
    request_data: QuestionsRequestModel,
) -> QuestionsResponseModel:
    try:
        s3_service = S3Service()
        tts_service = get_tts_service(model_name="openai")
        questions = await generate_interview_questions(interview_id, request_data)

        if request_data.interview_method != "chat":
            for question in questions.questions:
                question_text = question.question.question_text

                audio_bytes = await tts_service.generate_speech(question_text)

                object_key = (
                    f"test/users/{request_data.user_id}/interviews/{interview_id}/"
                    f"questions/question-{question.question_id}.mp3"
                )

                await s3_service.upload_s3_object(object_key, audio_bytes)

                question.question.s3_audio_url = object_key
        else:
            for question in questions.questions:
                question.question.s3_audio_url = None

        return questions
    except Exception as e:
        logging.error(f"Error processing questions for interview {interview_id}: {str(e)}")


def process_interview_evaluation(
    interview_id: int,
    request_data: EvaluationRequestModel,
) -> Union[TechnicalEvaluationResponseModel, PersonalEvaluationResponseModel]:
    prompt = generate_interview_evaluation_prompt(interview_id, request_data)

    merged_input = merge_questions_and_answers(request_data.questions, request_data.answers)
    merged_input_str = json.dumps(merged_input, ensure_ascii=False)

    generator = ContentGenerator(request_data=request_data)
    data = generator.invoke(prompt, merged_input_str, "evaluation")
    return data


async def process_answer_evaluation(
    interview_id: int,
    request_data: AnswerRequestModel,
) -> AnswerResponseModel:
    s3_service = get_s3_service()
    stt_service = get_stt_service(model_name="whisper")

    new_request_data, wpm = await generate_answer_evaluation_new_request_data(request_data, s3_service, stt_service)
    prompt = await generate_answer_evaluation_prompt(interview_id, new_request_data, wpm)

    merged_input = merge_question_and_answer(
        question=new_request_data.question,
        answer=new_request_data.answer,
    )
    merged_input_str = json.dumps(merged_input, ensure_ascii=False)

    generator = ContentGenerator(request_data=new_request_data)

    data = generator.invoke(prompt, merged_input_str, "answer")

    return data


async def generate_interview_questions(
    interview_id: int, request_data: QuestionsRequestModel
) -> QuestionsResponseModel:
    s3_service = get_s3_service()
    prompt = generate_questions_prompt(interview_id, request_data)

    cover_letter = ""
    if request_data.interview_mode == "real":
        file_objects = create_file_objects(request_data.file_paths)
        file_data = await s3_service.get_files_from_s3(file_objects)
        cover_letter = get_cover_letters_data(file_data)
        cover_letter = cover_letter

    generator = ContentGenerator(request_data=request_data)
    data = generator.invoke(prompt, cover_letter, "question")
    return data
