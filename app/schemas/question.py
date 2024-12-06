from typing import List, Optional

from pydantic import BaseModel

from app.schemas.base import BaseRequest


class QuestionDeatil(BaseModel):
    question_text: str
    s3_audio_url: Optional[str] = None
    s3_video_url: Optional[str] = None


# Base: Question의 최소 단위 데이터 모델
class QuestionBaseModel(BaseModel):
    question: QuestionDeatil
    question_excerpt: Optional[str] = None
    question_intent: str
    key_terms: List[str]


class QuestionBaseModelWithId(QuestionBaseModel):
    question_id: int


# Request:요청에 필요한 Request Body 모델
class QuestionsRequestModel(BaseRequest):
    question_count: int = 1
    file_paths: Optional[List[str]] = ["cover-letters/cover_letter_01.txt"]


# Reponse: 응답으로 나오는 Reponse 모델
class QuestionsResponseModel(BaseModel):
    user_id: int
    interview_id: int
    questions: List[QuestionBaseModel]
