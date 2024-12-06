from typing import Union

from fastapi import APIRouter, HTTPException

from app.schemas.answer import AnswerRequestModel
from app.schemas.evaluation import EvaluationRequestModel
from app.schemas.question import QuestionsRequestModel
from app.schemas.task import MessageQueueResponse
from app.services.tasks import (
    async_process_answer_evaluation,
    async_process_interview_questions,
    async_process_overall_evaluation,
)

router = APIRouter(prefix="/interview", tags=["Interview"])


@router.post("/{interview_id}/questions", tags=["Interview"], response_model=MessageQueueResponse)
async def create_interview_questions(
    interview_id: Union[int, str],
    request_data: QuestionsRequestModel,
):
    try:
        task = async_process_interview_questions.delay(interview_id, request_data.dict())
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
async def create_overall_evaluation(interview_id: Union[int, str], request_data: EvaluationRequestModel):
    try:
        task = async_process_overall_evaluation.delay(interview_id, request_data.dict())
        return {
            "message": "Evaluation processing started!",
            "task_id": task.id,
            "status": "processing",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating evaluation: {str(e)}")


@router.post("/{interview_id}/answer/{question_id}", tags=["Interview"], response_model=MessageQueueResponse)
async def create_answer_evaluation(
    interview_id: int,
    request_data: AnswerRequestModel,
):
    try:
        task = async_process_answer_evaluation.delay(interview_id, request_data.dict())
        return {
            "message": "Answer processing started!",
            "task_id": task.id,
            "status": "processing",
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing answer: {str(e)}")
