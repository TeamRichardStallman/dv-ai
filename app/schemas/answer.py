from typing import Literal, Optional, Union

from pydantic import BaseModel


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


class AnswerModel(BaseModel):
    answer_text: str = "테스트용 답변입니다."
    s3_audio_url: str = "test/questions/audio_1.mp3"
    s3_video_url: str


class AnswerRequest(BaseModel):
    interview_method: Literal["chat", "voice", "video"] = "voice"
    user_id: Union[int, str]
    answer: AnswerModel


class AnswerResponse(BaseModel):
    user_id: int
    interview_id: int
    question_id: int
    interview_method: str
    answer: AnswerDetail
