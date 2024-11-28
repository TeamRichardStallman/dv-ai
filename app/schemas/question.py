from typing import List, Optional

from pydantic import BaseModel

from app.schemas.base import BaseRequest


class QuestionDeatil(BaseModel):
    question_text: str
    s3_audio_url: Optional[str] = None
    s3_video_url: Optional[str] = None


class Question(BaseModel):
    question_id: int
    question: QuestionDeatil
    question_excerpt: Optional[str] = None
    question_intent: str
    key_terms: List[str]


class QuestionsResponse(BaseModel):
    questions: List[Question]


class QuestionsRequest(BaseRequest):
    question_count: int = 1
    file_paths: Optional[List[str]] = ["cover-letters/cover_letter_01.txt"]
