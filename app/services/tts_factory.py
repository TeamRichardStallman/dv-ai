from typing import Literal

from app.models.tts.elevenlabs import ElevenLabsTTSModel
from app.models.tts.google import GoogleTTSModel
from app.models.tts.openai import OpenAITTSModel
from app.models.tts.typecast import TypecastTTSModel


def get_tts_model(model_name: Literal["openai", "google", "typecast", "elevenlabs"]):
    if model_name == "openai":
        return OpenAITTSModel()
    elif model_name == "google":
        return GoogleTTSModel()
    elif model_name == "typecast":
        return TypecastTTSModel()
    elif model_name == "elevenlabs":  # ElevenLabs 추가
        return ElevenLabsTTSModel()
    else:
        raise ValueError(f"Unsupported TTS model: {model_name}")
