from pydantic import BaseModel
from typing import List


class Question(BaseModel):
    question_id: int
    question_excerpt: str
    question_text: str
    question_intent: str
    key_terms: List[str]


class QuestionsResponse(BaseModel):
    questions: List[Question]
