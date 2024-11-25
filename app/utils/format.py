import re


def clean_text(transcribed_text: str) -> str:
    cleaned_text = transcribed_text.replace("\n", " ")
    cleaned_text = re.sub(r"\s+", " ", cleaned_text).strip()
    return cleaned_text
