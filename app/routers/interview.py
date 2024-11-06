from fastapi import APIRouter, HTTPException
from app.services.ai_model import (
    generate_questions,
    evaluate_interview,
)
from app.models.questions_response import QuestionsResponse, QusetionsRequest
from app.models.evaluation_response import EvaluationResponse, EvaluationRequest

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
