from fastapi import APIRouter, HTTPException

from app.schemas.evaluation import EvaluationRequest, PersonalEvaluationResponse, TechnicalEvaluationResponse
from app.schemas.question import QuestionsRequest, QuestionsResponse
from app.services.ai_model import evaluate_interview, generate_questions
from app.tests.data import evaluation_test_data, questions_test_data

router = APIRouter(prefix="/interview", tags=["Interview"])


@router.post("/questions", tags=["Interview"], response_model=QuestionsResponse)
async def create_interview_questions(request_data: QuestionsRequest):
    try:
        questions = await generate_questions(request_data)
        return questions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating questions: {str(e)}")


@router.post("/evaluation", tags=["Interview"])
async def evaluate_interview_request(request_data: EvaluationRequest):
    try:
        if request_data.interview_type == "personal":
            evaluation = evaluate_interview(request_data)
            return PersonalEvaluationResponse(**evaluation)
        else:
            evaluation = evaluate_interview(request_data)
            return TechnicalEvaluationResponse(**evaluation)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating evaluation: {str(e)}")


@router.post("/questions-test", tags=["Interview"], response_model=QuestionsResponse)
async def create_interview_questions_test(request_data: QuestionsRequest):
    try:
        return questions_test_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating questions: {str(e)}")


@router.post("/evaluation-test", tags=["Interview"])
async def evaluate_interview_request_test(request_data: EvaluationRequest):
    try:
        if request_data.interview_type == "personal":
            return PersonalEvaluationResponse(**evaluation_test_data)
        else:
            return TechnicalEvaluationResponse(**evaluation_test_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating evaluation: {str(e)}")
