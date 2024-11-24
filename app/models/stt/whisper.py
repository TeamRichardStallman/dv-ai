import os
import tempfile

from openai import OpenAI

from app.core.config import Config

from .base import BaseSTTModel


class WhisperSTTModel(BaseSTTModel):
    def __init__(self):
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)

    async def transcribe(self, audio_file: bytes) -> str:
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
                temp_file.write(audio_file)
                temp_file_path = temp_file.name

            response = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=open(temp_file_path, "rb"),
                response_format="text",
            )

            return response
        except Exception as e:
            raise RuntimeError(f"Error transcribing audio with OpenAI Whisper API: {e}")
        finally:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
