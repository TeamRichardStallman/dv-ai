from app.models.tts.google import GoogleTTSModel
from app.models.tts.openai import OpenAITTSModel


def get_tts_model(model_name: str):
    if model_name == "openai":
        return OpenAITTSModel()
    elif model_name == "google":
        return GoogleTTSModel()
    else:
        raise ValueError(f"Unsupported TTS model: {model_name}")
