import httpx

from app.core.config import Config

from .base import BaseTTSModel


class ElevenLabsTTSModel(BaseTTSModel):
    def __init__(self):
        self.api_key = Config.ELEVENLABS_API_KEY  # ElevenLabs API 키
        self.api_url = "https://api.elevenlabs.io/v1/text-to-speech/"
        self.default_voice_id = Config.ELEVENLABS_VOICE_ID  # 원하는 음성 ID
        self.model_id = "eleven_multilingual_v2"  # 사용할 모델 ID

    async def synthesize(self, text: str, language_code: str = "ko") -> bytes:
        headers = {
            "xi-api-key": self.api_key,
            "Content-Type": "application/json",
        }

        payload = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {"stability": 0.65, "similarity_boost": 0.65, "use_speaker_boost": True},
        }

        # 요청 URL 생성
        url = f"{self.api_url}{self.default_voice_id}"

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, headers=headers, json=payload)
                response.raise_for_status()
                return response.content
        except httpx.HTTPStatusError as e:
            raise RuntimeError(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            raise RuntimeError(f"Error synthesizing audio with ElevenLabs: {e}")
