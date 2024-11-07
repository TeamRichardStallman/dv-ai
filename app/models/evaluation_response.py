from pydantic import BaseModel
from typing import List, Optional, Literal
from typing_extensions import TypedDict
from app.models.questions_response import QuestionsResponse


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


class Answer(BaseModel):
    question_id: int
    answer_text: str


class AnswerResponse(BaseModel):
    answers: List[Answer]


class EvaluationRequest(BaseModel):
    interview_mode: Literal["real", "general"] = "real"
    interview_type: Literal["technical", "personal"] = "technical"
    interview_method: Literal["chat", "voice", "video"] = "chat"
    job_role: Literal["frontend", "backend", "infra", "ai"] = "infra"
    questions: QuestionsResponse
    answers: AnswerResponse
    file_paths: Optional[List[str]] = ["cover-letters/cover_letter_01.txt"]
