from pydantic import BaseModel
from typing import List, Dict


class AnswerEvaluation(BaseModel):
    question_id: int
    score: int
    feedback_text: str


class OverallScore(BaseModel):
    score: int
    feedback_text: str


class OverallEvaluation(BaseModel):
    development_skill: OverallScore
    growth_potential: OverallScore
    work_attitude: OverallScore
    technical_depth: OverallScore


class EvaluationResponse(BaseModel):
    answer_evaluations: List[AnswerEvaluation]
    overall_evaluation: OverallEvaluation
