from pydantic import BaseModel
from typing import List

class Answer(BaseModel):
    question_id: int
    answer_text: str

class Question(BaseModel):
    question_id: int
    question_text: str

class EvaluationRequest(BaseModel):
    cover_letter: str
    user_data: dict 
    questions: List[Question]
    answers: List[Answer]

    class Config:
        schema_extra = {
            "example": {
                "cover_letter": "This is the cover letter text...",
                "user_data": {
                    "interview_type": "real",
                    "interview_focus": "technical",
                    "media_type": "text",
                    "job_role": "cloud",
                    "language": "ko",
                    "cover_letter_path": "/path/to/cover_letter.txt"
                },
                "questions": [
                    {
                        "question_id": 1,
                        "question_text": "What motivated you to apply for this position?"
                    },
                    {
                        "question_id": 2,
                        "question_text": "Describe your experience with cloud technologies."
                    }
                ],
                "answers": [
                    {
                        "question_id": 1,
                        "answer_text": "I was motivated by the challenge of working with cutting-edge cloud technologies."
                    },
                    {
                        "question_id": 2,
                        "answer_text": "I have hands-on experience with AWS and Google Cloud platforms."
                    }
                ]
            }
        }