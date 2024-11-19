from typing import List, Literal, Optional

from pydantic import BaseModel
from typing_extensions import TypedDict

from app.models.questions_response import QuestionsResponse


class ScoreDetail(BaseModel):
    score: int
    rationale: str


class Feedback(BaseModel):
    strengths: str
    improvement: str
    suggestion: str


class PersonalScores(TypedDict):
    teamwork: ScoreDetail
    communication: ScoreDetail
    problem_solving: ScoreDetail
    accountability: ScoreDetail
    growth_mindset: ScoreDetail


class TechnicalScores(TypedDict):
    appropriate_response: ScoreDetail
    logical_flow: ScoreDetail
    key_terms: ScoreDetail
    consistency: ScoreDetail
    grammatical_errors: ScoreDetail


class PersonalAnswerEvaluation(BaseModel):
    question_id: int
    scores: PersonalScores
    feedback: Feedback


class TechnicalAnswerEvaluation(BaseModel):
    question_id: int
    scores: TechnicalScores
    feedback: Feedback


class OverallScore(BaseModel):
    score: int
    feedback: str


class PersonalOverallEvaluation(BaseModel):
    company_fit: OverallScore
    adaptability: OverallScore
    interpersonal_skills: OverallScore
    growth_attitude: OverallScore


class TechnicalOverallEvaluation(BaseModel):
    job_fit: OverallScore
    growth_potential: OverallScore
    work_attitude: OverallScore
    technical_depth: OverallScore


class PersonalEvaluationResponse(BaseModel):
    answer_evaluations: List[PersonalAnswerEvaluation]
    overall_evaluation: PersonalOverallEvaluation


class TechnicalEvaluationResponse(BaseModel):
    answer_evaluations: List[TechnicalAnswerEvaluation]
    overall_evaluation: TechnicalOverallEvaluation


class Answer(BaseModel):
    question_id: int
    answer_text: str


class AnswerResponse(BaseModel):
    answers: List[Answer]


class EvaluationRequest(BaseModel):
    interview_mode: Literal["real", "general"] = "real"
    interview_type: Literal["technical", "personal"] = "technical"
    interview_method: Literal["chat", "voice", "video"] = "chat"
    job_role: Literal["frontend", "backend", "infra", "ai"] = "ai"
    questions: QuestionsResponse
    answers: AnswerResponse
    file_paths: Optional[List[str]] = ["cover-letters/SK_AI.txt"]
