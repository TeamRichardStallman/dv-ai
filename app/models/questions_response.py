from pydantic import BaseModel
from typing import List


class Question(BaseModel):
    question_id: int
    question_text: str
    source_sentence: str
    question_intent: str
    key_terms: List[str]


class QuestionsResponse(BaseModel):
    questions: List[Question]
