from app.models.stt.google import GoogleSTTModel
from app.models.stt.whisper import WhisperSTTModel


def get_stt_model(model_name: str):
    if model_name == "whisper":
        return WhisperSTTModel()
    elif model_name == "google":
        return GoogleSTTModel()
    else:
        raise ValueError(f"Unsupported STT model: {model_name}")
