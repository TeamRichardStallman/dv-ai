from typing import List, Optional, Union

from pydantic import BaseModel

from app.schemas.answer import ScoreDetail, Scores
from app.schemas.base import BaseRequest
from app.schemas.question import QuestionsResponse


class Feedback(BaseModel):
    strengths: str
    improvement: str
    suggestion: str


# EvaluationRequest에서만 쓸 AnswerResponse
class SimplifiedAnswerDetail(BaseModel):
    answer_text: str
    s3_audio_url: Optional[str]
    s3_video_url: Optional[str]
    scores: Scores
    feedback: Feedback


class SimplifiedAnswerResponse(BaseModel):
    question_id: int
    answer: SimplifiedAnswerDetail


class EvaluationRequest(BaseRequest):
    questions: QuestionsResponse
    answers: List[SimplifiedAnswerResponse]
    file_paths: Optional[List[str]] = ["cover-letters/SK_AI.txt"]


# 새로 추가된 overall evaluation 스키마
class TextTechnicalOverallEvaluation(BaseModel):
    job_fit: ScoreDetail
    growth_potential: ScoreDetail
    work_attitude: ScoreDetail
    technical_depth: ScoreDetail


class TextPersonalOverallEvaluation(BaseModel):
    company_fit: ScoreDetail
    adaptability: ScoreDetail
    interpersonal_skills: ScoreDetail
    growth_attitude: ScoreDetail


class VoiceOverallEvaluation(BaseModel):
    fluency: ScoreDetail
    clarity: ScoreDetail
    word_repetition: ScoreDetail


class OverallEvaluation(BaseModel):
    text_overall: Union[TextTechnicalOverallEvaluation, TextPersonalOverallEvaluation]
    voice_overall: VoiceOverallEvaluation


class EvaluationResponse(BaseModel):
    user_id: int
    interview_id: int
    overall_evaluation: OverallEvaluation
