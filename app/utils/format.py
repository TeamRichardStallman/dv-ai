import re

from pydantic import BaseModel


def clean_text(transcribed_text: str) -> str:
    cleaned_text = transcribed_text.replace("\n", " ")
    cleaned_text = re.sub(r"\s+", " ", cleaned_text).strip()
    return cleaned_text


def to_serializable(value):
    if isinstance(value, BaseModel):
        return value.model_dump()  # Pydantic 모델을 dict로 변환
    elif isinstance(value, dict):
        return {k: to_serializable(v) for k, v in value.items()}  # dict 내부 처리
    elif isinstance(value, list):
        return [to_serializable(v) for v in value]  # 리스트 내부 처리
    elif isinstance(value, tuple):
        return tuple(to_serializable(v) for v in value)  # 튜플 내부 처리
    elif hasattr(value, "__dict__"):  # 기타 사용자 정의 객체
        return to_serializable(value.__dict__)
    else:
        return value
