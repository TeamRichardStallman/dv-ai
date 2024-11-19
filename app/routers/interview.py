from typing import Union

from fastapi import APIRouter, HTTPException

from app.schemas.evaluation import EvaluationRequest, PersonalEvaluationResponse, TechnicalEvaluationResponse
from app.schemas.question import QuestionsRequest, QuestionsResponse
from app.services.interview_service import generate_interview_evaluation, generate_interview_questions
from app.tests.data import evaluation_test_data, questions_test_data

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
