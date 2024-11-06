from pydantic import BaseModel
from typing import List, Optional, Literal
from typing_extensions import TypedDict


class ScoreDetail(BaseModel):
    score: int
    rationale: str


class Feedback(BaseModel):
    strengths: str
    improvement: str
    suggestion: str


class Scores(TypedDict):
    appropriate_response: ScoreDetail
    logical_flow: ScoreDetail
    key_terms: ScoreDetail
    consistency: ScoreDetail
    grammatical_errors: ScoreDetail


class AnswerEvaluation(BaseModel):
    question_id: int
    scores: Scores
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


class EvaluationUserData(BaseModel):
    interview_mode: Literal["real", "general"]
    interview_type: Literal["technical", "personal"]
    interview_method: Literal["chat", "voice", "video"]
    job_role: Literal["frontend", "backend", "infra", "ai"]
    questions: str
    answers: str
    file_paths: Optional[List[str]]
