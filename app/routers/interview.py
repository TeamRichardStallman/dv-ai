from fastapi import APIRouter, File, UploadFile, HTTPException, Form
from app.services.ai_model import generate_questions_from_cover_letter
from app.models.questions_response import QuestionsResponse 

router = APIRouter(
    prefix="/interview",
    tags=["Interview"]
)

@router.post("/questions", response_model=QuestionsResponse)
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