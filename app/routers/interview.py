from fastapi import APIRouter, HTTPException, Form
from app.services.ai_model import (
    generate_questions,
    evaluate_interview,
)
from app.models.questions_response import QuestionsResponse, QuestionUserData
from app.models.evaluation_response import EvaluationResponse, EvaluationUserData
from typing import List, Optional, Literal

router = APIRouter(prefix="/interview", tags=["Interview"])


@router.post("/questions", tags=["Interview"], response_model=QuestionsResponse)
async def create_interview_questions(
    interview_mode: Literal["real", "general"] = Form(
        ..., description="Interview Mode: real(실전면접), general(모의면접)"
    ),
    interview_type: Literal["technical", "personal"] = Form(
        ..., description="Interview Type: technical(기술면접), personal(인성면접)"
    ),
    interview_method: Literal["chat", "voice", "video"] = Form(
        ..., description="Interview Method: chat(채팅), voice(음성), video(영상)"
    ),
    job_role: Literal["frontend", "backend", "infra", "ai"] = Form(
        ..., description="Job role: frontend, backend, infra, ai"
    ),
    file_paths: Optional[List[str]] = Form(
        ..., description="List of file paths, where each item represents a separate file path"
    ),
):
    user_data: QuestionUserData = {
        "interview_mode": interview_mode,
        "interview_type": interview_type,
        "interview_method": interview_method,
        "job_role": job_role,
        "file_paths": file_paths,
    }

    try:
        questions = await generate_questions(user_data)
        return questions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating questions: {str(e)}")


@router.post("/evaluation", tags=["Interview"], response_model=EvaluationResponse)
async def evaluate_interview_request(
    interview_mode: Literal["real", "general"] = Form(
        ..., description="Interview Mode: real(실전면접), general(모의면접)"
    ),
    interview_type: Literal["technical", "personal"] = Form(
        ..., description="Interview Type: technical(기술면접), personal(인성면접)"
    ),
    interview_method: Literal["chat", "voice", "video"] = Form(
        ..., description="Interview Method: chat(채팅), voice(음성), video(영상)"
    ),
    job_role: Literal["frontend", "backend", "infra", "ai"] = Form(
        ..., description="Job role: frontend, backend, infra, ai"
    ),
    questions: str = Form(..., description="List of questions as JSON string"),
    answers: str = Form(..., description="List of answers as JSON string"),
    file_paths: Optional[List[str]] = Form(
        ..., description="List of file paths, where each item represents a separate file path"
    ),
):

    user_data: EvaluationUserData = {
        "interview_mode": interview_mode,
        "interview_type": interview_type,
        "interview_method": interview_method,
        "job_role": job_role,
        "questions": questions,
        "answers": answers,
        "file_paths": file_paths,
    }

    try:
        evaluation = evaluate_interview(user_data)
        return evaluation
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating evaluation: {str(e)}")
