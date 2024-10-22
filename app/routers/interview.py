from fastapi import APIRouter
from pydantic import BaseModel

# 인터뷰 라우터 생성
router = APIRouter(
    prefix="/interview",
    tags=["Interview"]
)

# 요청 바디를 위한 데이터 모델
class InterviewRequest(BaseModel):
    candidate_name: str
    job_title: str

# 인터뷰 엔드포인트 생성
@router.post("/create")
async def create_interview(interview: InterviewRequest):
    return {"message": f"Interview created for {interview.candidate_name} applying for {interview.job_title}"}