from typing import Optional, Union

from pydantic import BaseModel

from app.schemas.base import BaseRequest
from app.schemas.question import QuestionBaseModelWithId


class ScoreDetail(BaseModel):
    score: int
    rationale: str


class TechnicalTextScores(BaseModel):
    appropriate_response: ScoreDetail
    logical_flow: ScoreDetail
    key_terms: ScoreDetail
    consistency: ScoreDetail
    grammatical_errors: ScoreDetail


class PersonalTextScores(BaseModel):
    teamwork: ScoreDetail
    communication: ScoreDetail
    problem_solving: ScoreDetail
    accountability: ScoreDetail
    growth_mindset: ScoreDetail


class VoiceScores(BaseModel):
    wpm: ScoreDetail
    stutter: ScoreDetail
    pronunciation: ScoreDetail


class Scores(BaseModel):
    text_scores: Union[TechnicalTextScores, PersonalTextScores]
    voice_scores: Optional[VoiceScores]


class Feedback(BaseModel):
    strengths: str
    improvement: str
    suggestion: str


class AnswerDetail(BaseModel):
    answer_text: str
    s3_audio_url: Union[str, None] = None
    s3_video_url: Union[str, None] = None
    scores: Scores
    feedback: Feedback


# Base: Answer의 최소 단위 데이터 모델
class AnswerBaseModel(BaseModel):
    answer_text: str = "테스트용 답변입니다."
    s3_audio_url: str = "questions/audio_1.mp3"
    s3_video_url: str


# Request:요청에 필요한 Request Body 모델
class AnswerRequestModel(BaseRequest):
    question: QuestionBaseModelWithId
    answer: AnswerBaseModel
    file_path: Union[str, None] = "cover-letters/SK_AI_01.txt"


# Request: 응답으로 나오는 Reponse 모델
class AnswerResponseModel(BaseModel):
    user_id: int
    interview_id: int
    interview_method: str
    question_id: int
    answer: AnswerDetail
