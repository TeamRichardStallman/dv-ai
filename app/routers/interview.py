from fastapi import APIRouter, File, UploadFile, HTTPException, Form
from app.services.ai_model import generate_questions_from_cover_letter, evaluate_interview
from app.models.questions_response import QuestionsResponse 
from app.models.evaluation_response import EvaluationResponse
from app.utils.merge import merge_questions_answers
import json

router = APIRouter(
    prefix="/interview",
    tags=["Interview"]
)

@router.post("/questions", tags=["Interview"], response_model=QuestionsResponse)
async def create_interview_questions(
    cover_letter: UploadFile = File(..., description="Cover letter as a text file"),
    interview_type: str = Form(..., description="Interview type: real(실전면접), general(모의면접)"),
    interview_focus: str = Form(..., description="Interview focus: technical, personality"),
    media_type: str = Form(..., description="Media type: text, audio, video"),
    job_role: str = Form(..., description="Job role: frontend, backend, cloud, ai"),
    language: str = Form("ko", description="Language of the interview"),
):
    cover_letter_content = await cover_letter.read()
    
    user_data = {
            "interview_type": interview_type,
            "interview_focus": interview_focus,
            "media_type": media_type,
            "job_role": job_role,
            "language": language,
        }

    try:
        questions = generate_questions_from_cover_letter(cover_letter_content.decode("utf-8"), user_data)
        return {"questions": questions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating questions: {str(e)}")

@router.post("/evaluation", tags=["Interview"], response_model=EvaluationResponse)
async def evaluate_interview_request(
    cover_letter: UploadFile = File(..., description="Cover letter as a text file"),
    questions: UploadFile = File(..., description="Questions as a JSON file"),
    answers: UploadFile = File(..., description="Answers as a JSON file"),
    interview_type: str = Form(..., description="Interview type: real(실전면접), general(모의면접)"),
    interview_focus: str = Form(..., description="Interview focus: technical, personality"),
    media_type: str = Form(..., description="Media type: text, audio, video"),
    job_role: str = Form(..., description="Job role: frontend, backend, cloud, ai"),
    language: str = Form("ko", description="Language of the interview"),
):
    try:
        cover_letter_content = await cover_letter.read()
        questions_content = await questions.read()
        answers_content = await answers.read()
        
        cover_letter_data = cover_letter_content.decode("utf-8")
        questions_data = json.loads(questions_content.decode("utf-8"))
        answers_data = json.loads(answers_content.decode("utf-8"))

        merged_input = merge_questions_answers(questions_data, answers_data)

        user_data = {
            "interview_type": interview_type,
            "interview_focus": interview_focus,
            "media_type": media_type,
            "job_role": job_role,
            "language": language,
        }

        evaluation_result = evaluate_interview(cover_letter_data, merged_input, user_data)

        return evaluation_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating evaluation: {str(e)}")