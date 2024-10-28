from fastapi import APIRouter, File, UploadFile, HTTPException, Form
from app.services.ai_model import (
    generate_questions,
    evaluate_interview,
)
from app.models.questions_response import QuestionsResponse
from app.models.evaluation_response import EvaluationResponse
from app.utils.merge import merge_questions_and_answers
import json

router = APIRouter(prefix="/interview", tags=["Interview"])


@router.post("/questions", tags=["Interview"], response_model=QuestionsResponse)
async def create_interview_questions(
    cover_letter: UploadFile = File(..., description="Cover letter as a text file"),
    interview_mode: str = Form(..., description="Interview Mode: real(실전면접), general(모의면접)"),
    interview_type: str = Form(..., description="Interview Type: technical(기술면접), personal(인성면접)"),
    interview_method: str = Form(..., description="Interview Method: chat(채팅), voice(음성), video(영상)"),
    job_role: str = Form(..., description="Job role: frontend, backend, infra, ai"),
):
    cover_letter_content = await cover_letter.read()
    cover_letter_data = cover_letter_content.decode("utf-8")

    user_data = {
        "interview_mode": interview_mode,
        "interview_type": interview_type,
        "interview_method": interview_method,
        "job_role": job_role,
    }

    try:
        questions = generate_questions(cover_letter_data, user_data)
        return questions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating questions: {str(e)}")


@router.post("/evaluation", tags=["Interview"], response_model=EvaluationResponse)
async def evaluate_interview_request(
    cover_letter: UploadFile = File(..., description="Cover letter as a text file"),
    questions: UploadFile = File(..., description="Questions as a JSON file"),
    answers: UploadFile = File(..., description="Answers as a JSON file"),
    interview_mode: str = Form(..., description="Interview Mode: real(실전면접), general(모의면접)"),
    interview_type: str = Form(..., description="Interview Type: technical(기술면접), personal(인성면접)"),
    interview_method: str = Form(..., description="Interview Method: chat(채팅), voice(음성), video(영상)"),
    job_role: str = Form(..., description="Job role: frontend, backend, infra, ai"),
):
    # cover_letter_content = await cover_letter.read()
    ruestions_content = await questions.read()
    answers_content = await answers.read()

    # cover_letter_data = cover_letter_content.decode("utf-8")
    questions_data = json.loads(ruestions_content.decode("utf-8"))
    answers_data = json.loads(answers_content.decode("utf-8"))

    merged_input = merge_questions_and_answers(questions_data, answers_data)

    user_data = {
        "interview_mode": interview_mode,
        "interview_type": interview_type,
        "interview_method": interview_method,
        "job_role": job_role,
    }

    try:
        evaluation = evaluate_interview(merged_input, user_data)
        return evaluation
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating evaluation: {str(e)}")
