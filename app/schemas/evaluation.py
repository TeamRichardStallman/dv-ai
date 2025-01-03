from typing import List, Union

from pydantic import BaseModel

from app.schemas.answer import PersonalTextScores, ScoreDetail, TechnicalTextScores, VoiceScores
from app.schemas.base import BaseRequest
from app.schemas.question import QuestionBaseModelWithId


class Feedback(BaseModel):
    strengths: str
    improvement: str
    suggestion: str


class Scores(BaseModel):
    text_scores: Union[TechnicalTextScores, PersonalTextScores]
    voice_scores: Union[VoiceScores, None]


class SimplifiedAnswerDetail(BaseModel):
    answer_text: str
    s3_audio_url: Union[str, None] = None
    s3_video_url: Union[str, None] = None
    scores: Scores
    feedback: Feedback


class AnswerPartialResponse(BaseModel):
    question_id: int
    answer: SimplifiedAnswerDetail


# Request:요청에 필요한 Request Body 모델
class EvaluationRequestModel(BaseRequest):
    questions: List[QuestionBaseModelWithId]
    answers: List[AnswerPartialResponse]
    file_paths: Union[List[str], None] = ["cover-letters/SK_AI_01.txt"]


class TechnicalTextOverallEvaluation(BaseModel):
    job_fit: ScoreDetail
    growth_potential: ScoreDetail
    work_attitude: ScoreDetail
    technical_depth: ScoreDetail


class PersonalTextOverallEvaluation(BaseModel):
    company_fit: ScoreDetail
    adaptability: ScoreDetail
    interpersonal_skills: ScoreDetail
    growth_attitude: ScoreDetail


class VoiceOverallEvaluation(BaseModel):
    fluency: ScoreDetail
    clarity: ScoreDetail
    word_repetition: ScoreDetail


class TechnicalOverallEvaluation(BaseModel):
    text_overall: TechnicalTextOverallEvaluation
    voice_overall: Union[VoiceOverallEvaluation, None]


class PersonalOverallEvaluation(BaseModel):
    text_overall: PersonalTextOverallEvaluation
    voice_overall: Union[VoiceOverallEvaluation, None]


# Reponse: 응답으로 나오는 Reponse 모델
class TechnicalEvaluationResponseModel(BaseModel):
    user_id: int
    interview_id: int
    overall_evaluation: TechnicalOverallEvaluation


# Reponse: 응답으로 나오는 Reponse 모델
class PersonalEvaluationResponseModel(BaseModel):
    user_id: int
    interview_id: int
    overall_evaluation: PersonalOverallEvaluation
