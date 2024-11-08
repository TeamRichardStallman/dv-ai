from fastapi import APIRouter, HTTPException
from app.services.ai_model import generate_questions, evaluate_interview
from app.models.questions_response import QuestionsResponse, QuestionsRequest
from app.models.evaluation_response import PersonalEvaluationResponse, TechnicalEvaluationResponse, EvaluationRequest
from app.temp.test_data import questions_test_data, evaluation_test_data

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