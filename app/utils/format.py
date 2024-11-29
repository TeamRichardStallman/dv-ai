import re

from pydantic import BaseModel


def clean_text(transcribed_text: str) -> str:
    cleaned_text = transcribed_text.replace("\n", " ")
    cleaned_text = re.sub(r"\s+", " ", cleaned_text).strip()
    return cleaned_text


def to_serializable(value):
    if isinstance(value, BaseModel):
        return value.model_dump()
    elif isinstance(value, dict):
        return {k: to_serializable(v) for k, v in value.items()}
    elif isinstance(value, list):
        return [to_serializable(v) for v in value]
    elif isinstance(value, tuple):
        return tuple(to_serializable(v) for v in value)
    elif hasattr(value, "__dict__"):
        return to_serializable(value.__dict__)
    else:
        return value
