from pydantic import BaseModel
from typing import List, Dict


class AnswerEvaluation(BaseModel):
    question_id: int
    score: int
    feedback_text: str


class OverallEvaluation(BaseModel):
    development_skill: AnswerEvaluation
    growth_potential: AnswerEvaluation
    work_attitude: AnswerEvaluation
    technical_depth: AnswerEvaluation


class EvaluationResponse(BaseModel):
    answer_evaluations: List[AnswerEvaluation]
    overall_evaluation: OverallEvaluation