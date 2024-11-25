from typing import Literal, Union

from pydantic import BaseModel


class AnswerModel(BaseModel):
    answer_text: str = "테스트용 답변입니다."
    s3_audio_url: str = "test/questions/audio_1.mp3"
    s3_video_url: str


class AnswerRequest(BaseModel):
    interview_method: Literal["CHAT", "VOICE", "VIDEO"] = "VOICE"
    user_id: Union[int, str]
    answer: AnswerModel
