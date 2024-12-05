from typing import Union

from fastapi import APIRouter, HTTPException

from app.schemas.answer import AnswerRequest
from app.schemas.evaluation import EvaluationRequest
from app.schemas.question import QuestionsRequest
from app.schemas.task import MessageQueueResponse
from app.services.tasks import async_process_answer, async_process_evaluation, async_process_questions

# from app.services.interview_service import process_single_evaluation

router = APIRouter(prefix="/interview", tags=["Interview"])


@router.post("/{interview_id}/questions", tags=["Interview"], response_model=MessageQueueResponse)
async def create_interview_questions(
    interview_id: Union[int, str],
    request_data: QuestionsRequest,
):
    try:
        task = async_process_questions.delay(interview_id, request_data.dict())
        return {
            "message": "Question processing started!",
            "task_id": task.id,
            "status": "processing",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating questions: {str(e)}")


@router.post(
    "/{interview_id}/evaluation",
    tags=["Interview"],
    response_model=MessageQueueResponse,
)
async def create_interview_evaluation(interview_id: Union[int, str], request_data: EvaluationRequest):
    try:
        task = async_process_evaluation.delay(interview_id, request_data.dict())
        return {
            "message": "Evaluation processing started!",
            "task_id": task.id,
            "status": "processing",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating evaluation: {str(e)}")


@router.post("/{interview_id}/answer/{question_or_answer_id}", tags=["Interview"], response_model=MessageQueueResponse)
async def create_asnwer_text_from_answer_audio(
    interview_id: int,
    question_or_answer_id: int,
    request_data: AnswerRequest,
):
    try:
        task = async_process_answer.delay(interview_id, question_or_answer_id, request_data.dict())
        return {
            "message": "Answer processing started!",
            "task_id": task.id,
            "status": "processing",
        }
        # return await process_single_evaluation(interview_id, question_or_answer_id, request_data, s3_service, stt_service)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing answer: {str(e)}")
