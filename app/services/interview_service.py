import json
import logging
import os
from typing import Union

import weave
from dotenv import load_dotenv
from openai import OpenAI

from app.models.openai.gpt import ContentGenerator
from app.schemas.answer import (
    AnswerDetail,
    AnswerRequest,
    AnswerResponse,
    Feedback,
    ScoreDetail,
    Scores,
    TextScores,
    VoiceScores,
)
from app.schemas.evaluation import EvaluationRequest, PersonalEvaluationResponse, TechnicalEvaluationResponse
from app.schemas.question import QuestionsRequest, QuestionsResponse
from app.services.evaluation_service import generate_evaluation_prompt, generate_single_evaluation_prompt
from app.services.question_service import generate_questions_prompt
from app.services.s3_service import S3Service
from app.services.stt_service import STTService
from app.services.tts_service import TTSService
from app.utils.format import clean_text
from app.utils.generate import create_file_objects, get_cover_letters_data
from app.utils.merge import merge_questions_and_answers, merge_single_question_and_answer

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client_gpt = OpenAI(api_key=OPENAI_API_KEY)

weave.init("ticani0610-no/prompt-test")

logging.basicConfig(level=logging.INFO)


async def process_questions(
    interview_id: Union[int, str],
    request_data: QuestionsRequest,
    s3_service: S3Service,
    tts_service: TTSService,
) -> QuestionsResponse:
    try:
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


def process_evaluation(
    interview_id: int,
    user_data: EvaluationRequest,
) -> Union[TechnicalEvaluationResponse, PersonalEvaluationResponse]:
    prompt = generate_evaluation_prompt(interview_id, user_data)

    merged_input = merge_questions_and_answers(user_data.questions, user_data.answers)
    merged_input_str = json.dumps(merged_input, ensure_ascii=False)

    generator = ContentGenerator(user_data=user_data)
    data = generator.invoke(prompt, merged_input_str, "evaluation")
    return data


async def process_single_evaluation(
    interview_id: int,
    question_or_answer_id: int,
    request_data: AnswerRequest,
    s3_service: S3Service,
    stt_service: STTService,
) -> AnswerResponse:

    default_text_scores = TextScores(
        appropriate_response=ScoreDetail(score=0, rationale=""),
        logical_flow=ScoreDetail(score=0, rationale=""),
        key_terms=ScoreDetail(score=0, rationale=""),
        consistency=ScoreDetail(score=0, rationale=""),
        grammatical_errors=ScoreDetail(score=0, rationale=""),
    )

    default_voice_scores = VoiceScores(
        wpm=ScoreDetail(score=0, rationale=""),
        stutter=ScoreDetail(score=0, rationale=""),
        pronunciation=ScoreDetail(score=0, rationale=""),
    )

    default_scores = Scores(
        text_scores=default_text_scores,
        voice_scores=default_voice_scores,
    )

    default_feedback = Feedback(
        strengths="",
        improvement="",
        suggestion="",
    )

    answer = AnswerDetail(
        answer_text="",
        s3_audio_url=None,
        s3_video_url=None,
        scores=default_scores,
        feedback=default_feedback,
    )

    if request_data.interview_method == "chat":
        answer.answer_text = request_data.answer.answer_text

    if request_data.interview_method != "chat":
        s3_audio_url = request_data.answer.s3_audio_url
        if not s3_audio_url:
            raise ValueError("s3_audio_url is required")

        audio_file = await s3_service.get_s3_object(s3_audio_url)

        transcribed_text, wpm = await stt_service.transcribe_audio(audio_file)
        cleaned_text = clean_text(transcribed_text)

        merged_input = merge_single_question_and_answer(
            question=request_data.question,
            answer=request_data.answer,
        )

        merged_input["answer_text"] = cleaned_text
        merged_input_str = json.dumps(merged_input, ensure_ascii=False)

        user_data = {
            "user_id": request_data.user_id,
            "job_role": request_data.job_role,
            "interview_type": request_data.interview_type,
            "interview_mode": request_data.interview_mode,
            "interview_method": request_data.interview_method,
        }

        prompt = generate_single_evaluation_prompt(interview_id, user_data, wpm)

        generator = ContentGenerator(user_data=user_data)
        evaluation_result = generator.invoke(prompt, merged_input_str, "evaluation")

        answer.answer_text = cleaned_text
        answer.s3_audio_url = s3_audio_url
        answer.scores = evaluation_result.get("scores", default_scores)
        answer.feedback = evaluation_result.get("feedback", default_feedback)

        return {
            "user_id": request_data.user_id,
            "interview_id": interview_id,
            "question_id": question_or_answer_id,
            "interview_method": request_data.interview_method,
            "answer": answer,
        }


async def generate_interview_questions(interview_id: int, user_data: QuestionsRequest) -> QuestionsResponse:
    s3_service = S3Service()
    prompt = generate_questions_prompt(interview_id, user_data)

    cover_letter = ""
    if user_data.interview_mode == "real":
        file_objects = create_file_objects(user_data.file_paths)
        file_data = await s3_service.get_files_from_s3(file_objects)
        cover_letter = get_cover_letters_data(file_data)
        cover_letter = cover_letter

    generator = ContentGenerator(user_data=user_data)
    data = generator.invoke(prompt, cover_letter, "question")
    return data
