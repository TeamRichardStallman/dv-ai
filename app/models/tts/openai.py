from openai import OpenAI

from app.core.config import Config

from .base import BaseTTSModel


class OpenAITTSModel(BaseTTSModel):
    def __init__(self):
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)

    async def synthesize(self, text: str) -> bytes:
        try:

            response = self.client.audio.speech.create(
                model="tts-1",
                voice="alloy",
                input=text,
            )

            return response.content
        except Exception as e:
            raise RuntimeError(f"Error synthesizing audio with OpenAI TTS: {e}")
