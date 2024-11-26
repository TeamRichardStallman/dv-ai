import requests

from app.core.config import Config

from .base import BaseTTSModel


class TypecastTTSModel(BaseTTSModel):
    def __init__(self):
        self.api_key = Config.TYPECAST_API_KEY
        self.base_url = "https://api.typecast.ai/v1/tts"

    async def synthesize(self, text: str, language_code: str = "en-US") -> bytes:
        try:
            payload = {
                "text": text,
                "language": language_code,
                "voice": "default",  # Replace with a valid voice for the Typecast API
            }

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }

            response = requests.post(self.base_url, json=payload, headers=headers)
            response.raise_for_status()

            return response.content
        except Exception as e:
            raise RuntimeError(f"Error synthesizing audio with Typecast TTS: {e}")
