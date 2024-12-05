from typing import Union

from fastapi import APIRouter, Depends, HTTPException

from app.schemas.answer import AnswerRequest, AnswerResponse
from app.schemas.evaluation import EvaluationRequest, PersonalEvaluationResponse, TechnicalEvaluationResponse
from app.schemas.question import QuestionsRequest, QuestionsResponse
from app.services.interview_service import process_single_evaluation, process_evaluation, process_questions
from app.services.s3_service import S3Service, get_s3_service
from app.services.stt_service import STTService, get_stt_service
from app.services.tts_service import TTSService, get_tts_service
from app.tests.data import evaluation_test_data, questions_test_data

router = APIRouter(prefix="/interview", tags=["Interview"])


@router.post("/{interview_id}/questions", tags=["Interview"], response_model=QuestionsResponse)
async def create_interview_questions(
    interview_id: Union[int, str],
    request_data: QuestionsRequest,
    s3_service: S3Service = Depends(get_s3_service),
    tts_service: TTSService = Depends(get_tts_service),
):
    try:
        result = await process_questions(interview_id, request_data, s3_service, tts_service)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating questions: {str(e)}")


@router.post(
    "/{interview_id}/evaluation",
    tags=["Interview"],
    response_model=Union[TechnicalEvaluationResponse, PersonalEvaluationResponse],
)
async def create_interview_evaluation(interview_id: Union[int, str], request_data: EvaluationRequest):
    try:
        result = process_evaluation(interview_id, request_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating evaluation: {str(e)}")


@router.post("/{interview_id}/questions-test", tags=["Interview"], response_model=QuestionsResponse)
async def create_interview_questions_test():
    try:
        return questions_test_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating questions: {str(e)}")


@router.post(
    "/{interview_id}/evaluation-test",
    tags=["Interview"],
    response_model=Union[TechnicalEvaluationResponse, PersonalEvaluationResponse],
)
async def create_interview_evaluation_test():
    try:
        return evaluation_test_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating evaluation: {str(e)}")


@router.post("/{interview_id}/answer/{question_or_answer_id}", tags=["Interview"], response_model=AnswerResponse)
async def create_asnwer_text_from_answer_audio(
    interview_id: int,
    question_or_answer_id: int,
    request_data: AnswerRequest,
    s3_service: S3Service = Depends(get_s3_service),
    stt_service: STTService = Depends(get_stt_service),
):
    try:
        return await process_single_evaluation(interview_id, question_or_answer_id, request_data, s3_service, stt_service)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing answer: {str(e)}")
