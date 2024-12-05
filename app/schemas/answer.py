from typing import Optional

from pydantic import BaseModel

from app.schemas.base import BaseRequest
from app.schemas.question import QuestionBaseModel


class ScoreDetail(BaseModel):
    score: int
    rationale: str


class TextScores(BaseModel):
    appropriate_response: ScoreDetail
    logical_flow: ScoreDetail
    key_terms: ScoreDetail
    consistency: ScoreDetail
    grammatical_errors: ScoreDetail


class VoiceScores(BaseModel):
    wpm: ScoreDetail
    stutter: ScoreDetail
    pronunciation: ScoreDetail


class Scores(BaseModel):
    text_scores: TextScores
    voice_scores: Optional[VoiceScores]


class Feedback(BaseModel):
    strengths: str
    improvement: str
    suggestion: str


class AnswerDetail(BaseModel):
    answer_text: str
    s3_audio_url: Optional[str]
    s3_video_url: Optional[str]
    scores: Scores
    feedback: Feedback


# Base: Answer의 최소 단위 데이터 모델
class AnswerBaseModel(BaseModel):
    answer_text: str = "테스트용 답변입니다."
    s3_audio_url: str = "test/questions/audio_1.mp3"
    s3_video_url: str


# Request:요청에 필요한 Request Body 모델
class AnswerRequestModel(BaseRequest):
    question: QuestionBaseModel
    answer: AnswerBaseModel


# Request: 응답으로 나오는 Reponse 모델
class AnswerResponseModel(BaseModel):
    user_id: int
    interview_id: int
    question_id: int
    interview_method: str
    answer: AnswerDetail
