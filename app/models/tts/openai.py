import httpx

from app.core.config import Config

from .base import BaseTTSModel


class OpenAITTSModel(BaseTTSModel):
    def __init__(self):
        self.api_key = Config.OPENAI_API_KEY
        self.api_url = "https://api.openai.com/v1/audio/speech"

    async def synthesize(self, text: str) -> bytes:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": "tts-1",
            "voice": "alloy",
            "input": text,
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(self.api_url, headers=headers, json=payload)
                response.raise_for_status()
                return response.content
        except Exception as e:
            raise RuntimeError(f"Error synthesizing audio with OpenAI TTS: {e}")
