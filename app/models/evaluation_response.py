from pydantic import BaseModel
from typing import Dict, List


class ScoreDetail(BaseModel):
    score: int
    rationale: str


class Feedback(BaseModel):
    strengths: str
    improvement: str
    suggestion: str


class AnswerEvaluation(BaseModel):
    question_id: int
    scores: Dict[str, ScoreDetail]
    feedback: Feedback


class OverallScore(BaseModel):
    score: int
    feedback: str


class OverallEvaluation(BaseModel):
    job_fit: OverallScore
    growth_potential: OverallScore
    work_attitude: OverallScore
    technical_depth: OverallScore


class EvaluationResponse(BaseModel):
    answer_evaluations: List[AnswerEvaluation]
    overall_evaluation: OverallEvaluation
