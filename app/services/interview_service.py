import json
import os
from typing import Union

import weave
from dotenv import load_dotenv
from openai import OpenAI

from app.models.openai.gpt import ContentGenerator
from app.schemas.evaluation import EvaluationRequest, PersonalAnswerEvaluation, TechnicalAnswerEvaluation
from app.schemas.question import QuestionsRequest, QuestionsResponse
from app.services.evaluation_service import generate_evaluation_prompt
from app.services.question_service import generate_questions_prompt
from app.services.s3_service import S3Service
from app.services.stt_service import STTService
from app.services.tts_service import TTSService
from app.utils.format import clean_text
from app.utils.generate import create_file_objects, get_cover_letters_data
from app.utils.merge import merge_questions_and_answers

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client_gpt = OpenAI(api_key=OPENAI_API_KEY)

weave.init("ticani0610-no/prompt-test")


async def process_questions(
    interview_id: Union[int, str],
    request_data: QuestionsRequest,
    s3_service: S3Service,
    tts_service: TTSService,
) -> QuestionsResponse:
    questions = await generate_interview_questions(request_data)

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


async def process_answer(
    interview_id: int,
    question_or_answer_id: int,
    request_data,
    s3_service: S3Service,
    stt_service: STTService,
):
    if request_data.interview_method == "CHAT":
        return {
            "user_id": request_data.user_id,
            "interview_id": interview_id,
            "question_or_answer_id": question_or_answer_id,
            "answer_text": request_data.answer.answer_text,
        }

    s3_audio_url = request_data.answer.s3_audio_url
    if not s3_audio_url:
        raise ValueError("s3_audio_url is required")

    audio_file = await s3_service.get_s3_object(s3_audio_url)
    transcribed_text = await stt_service.transcribe_audio(audio_file)

    return {
        "user_id": request_data.user_id,
        "interview_id": interview_id,
        "question_or_answer_id": question_or_answer_id,
        "answer_text": clean_text(transcribed_text),
    }


async def generate_interview_questions(user_data: QuestionsRequest) -> QuestionsResponse:
    s3_service = S3Service()
    prompt = generate_questions_prompt(user_data)

    file_objects = create_file_objects(user_data.file_paths)
    file_data = await s3_service.get_files_from_s3(file_objects)
    cover_letter = get_cover_letters_data(file_data)
    cover_letter = cover_letter or ""

    generator = ContentGenerator(user_data=user_data)
    data = generator.invoke(prompt, cover_letter, "question")
    return data


def generate_interview_evaluation(
    user_data: EvaluationRequest,
) -> Union[TechnicalAnswerEvaluation, PersonalAnswerEvaluation]:
    prompt = generate_evaluation_prompt(user_data)

    merged_input = merge_questions_and_answers(user_data.questions, user_data.answers)
    merged_input_str = json.dumps(merged_input, ensure_ascii=False)

    generator = ContentGenerator(user_data=user_data)
    data = generator.invoke(prompt, merged_input_str, "evaluation")
    return data
