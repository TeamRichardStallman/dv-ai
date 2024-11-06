from pydantic import BaseModel
from typing import List, Optional, Literal


class Question(BaseModel):
    question_id: int
    question_excerpt: Optional[str]
    question_text: str
    question_intent: str
    key_terms: List[str]


class QuestionsResponse(BaseModel):
    questions: List[Question]


class QusetionsRequest(BaseModel):
    interview_mode: Literal["real", "general"]
    interview_type: Literal["technical", "personal"]
    interview_method: Literal["chat", "voice", "video"]
    job_role: Literal["frontend", "backend", "infra", "ai"]
    file_paths: Optional[List[str]]
