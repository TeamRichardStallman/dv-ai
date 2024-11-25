from typing import Union

from fastapi import APIRouter, Depends, HTTPException

from app.schemas.answer import AnswerRequest
from app.schemas.evaluation import EvaluationRequest, PersonalEvaluationResponse, TechnicalEvaluationResponse
from app.schemas.question import QuestionsRequest, QuestionsResponse
from app.services.interview_service import generate_interview_evaluation, generate_interview_questions
from app.services.s3_service import S3Service, get_s3_service
from app.services.stt_service import STTService, get_stt_service
from app.tests.data import evaluation_test_data, questions_test_data
from app.utils.format import clean_text

router = APIRouter(prefix="/interview", tags=["Interview"])


@router.post("/questions", tags=["Interview"], response_model=QuestionsResponse)
async def create_interview_questions(request_data: QuestionsRequest):
    try:
        questions = await generate_interview_questions(request_data)
        return questions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating questions: {str(e)}")


@router.post(
    "/evaluation",
    tags=["Interview"],
    response_model=Union[
        TechnicalEvaluationResponse,
        PersonalEvaluationResponse,
    ],
)
async def create_interview_evaluation(request_data: EvaluationRequest):
    try:
        evaluation = generate_interview_evaluation(request_data)
        return evaluation
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating evaluation: {str(e)}")


@router.post("/questions-test", tags=["Interview"], response_model=QuestionsResponse)
async def create_interview_questions_test():
    try:
        return questions_test_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating questions: {str(e)}")


@router.post(
    "/evaluation-test",
    tags=["Interview"],
    response_model=Union[
        TechnicalEvaluationResponse,
        PersonalEvaluationResponse,
    ],
)
async def create_interview_evaluation_test():
    try:
        return evaluation_test_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating evaluation: {str(e)}")


@router.post("/{interview_id}/answer/{question_or_answer_id}", tags=["Interview"])
async def create_asnwer_text_from_answer_audio(
    interview_id: int,
    question_or_answer_id: int,
    request_data: AnswerRequest,
    s3_service: S3Service = Depends(get_s3_service),
    stt_service: STTService = Depends(get_stt_service),
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
        raise HTTPException(status_code=400, detail="s3_audio_url is required")

    audio_file = await s3_service.get_s3_object(s3_audio_url)

    transcribed_text = await stt_service.transcribe_audio(audio_file)

    data_to_post = {
        "user_id": request_data.user_id,
        "interview_id": interview_id,
        "question_or_answer_id": question_or_answer_id,
        "answer_text": clean_text(transcribed_text),
    }

    return data_to_post
