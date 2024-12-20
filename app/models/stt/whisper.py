import os
import tempfile

from openai import OpenAI

from app.core.config import Config
from app.utils.wpm import calculate_wpm

from .base import BaseSTTModel


class WhisperSTTModel(BaseSTTModel):
    def __init__(self):
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)

    async def transcribe(self, audio_file: bytes):
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
                temp_file.write(audio_file)
                temp_file_path = temp_file.name

            response = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=open(temp_file_path, "rb"),
                response_format="verbose_json",
                timestamp_granularities=["word"],
            )

            wpm = calculate_wpm(response.to_dict())

            return response.to_dict().get("text"), wpm
        except Exception as e:
            raise RuntimeError(f"Error transcribing audio with OpenAI Whisper API: {e}")
        finally:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
