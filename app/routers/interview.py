from fastapi import APIRouter, HTTPException
from app.services.ai_model import (
    generate_questions,
    evaluate_interview,
)
from app.models.questions_response import QuestionsResponse, QusetionsRequest
from app.models.evaluation_response import EvaluationResponse, EvaluationRequest
from app.temp.test_data import questions_test_data, evaluation_test_data

router = APIRouter(prefix="/interview", tags=["Interview"])


@router.post("/questions", tags=["Interview"], response_model=QuestionsResponse)
async def create_interview_questions(request_data: QusetionsRequest):
    try:
        questions = await generate_questions(request_data)
        return questions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating questions: {str(e)}")


@router.post("/evaluation", tags=["Interview"], response_model=EvaluationResponse)
async def evaluate_interview_request(request_data: EvaluationRequest):
    try:
        evaluation = evaluate_interview(request_data)
        return evaluation
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating evaluation: {str(e)}")


@router.post("/questions-test", tags=["Interview"], response_model=QuestionsResponse)
async def create_interview_questions_test(request_data: QusetionsRequest):
    try:
        return questions_test_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating questions: {str(e)}")


@router.post("/evaluation-test", tags=["Interview"], response_model=EvaluationResponse)
async def evaluate_interview_request_test(request_data: EvaluationRequest):
    try:
        return evaluation_test_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating evaluation: {str(e)}")
