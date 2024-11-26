import json
import time

import requests

from app.core.config import Config

from .base import BaseTTSModel


class TypecastTTSModel(BaseTTSModel):
    def __init__(self):
        self.api_url = "https://typecast.ai/api/speak"
        self.auth_token = Config.TYPECAST_API_TOKEN

    async def synthesize(self, text: str) -> bytes:
        try:
            payload = json.dumps(
                {
                    "actor_id": "5c547544fcfee90007fed455",
                    "text": text.strip(),
                    "lang": "auto",
                    "tempo": 1,
                    "volume": 100,
                    "pitch": 0,
                    "xapi_hd": True,
                    "max_seconds": 60,
                    "model_version": "latest",
                    "xapi_audio_format": "mp3",
                },
                indent=4,
                ensure_ascii=False,
            )

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.auth_token}",
            }

            print("API URL:", self.api_url)
            print("Headers:", headers)
            print("Payload:", payload)

            response = requests.post(self.api_url, headers=headers, data=payload)
            response.raise_for_status()
            print("Response JSON:", response.json())

            speak_v2_url = response.json().get("result", {}).get("speak_v2_url")
            if not speak_v2_url:
                raise RuntimeError("Typecast API response is missing the 'speak_v2_url' field.")
            print("Speak V2 URL:", speak_v2_url)

            audio_download_url = self._get_audio_download_url(speak_v2_url, headers)
            print("Audio Download URL:", audio_download_url)

            audio_content = self._download_audio(audio_download_url)
            print("Audio Content Length:", len(audio_content))

            return audio_content

        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Error interacting with Typecast API: {e}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error during Typecast TTS synthesis: {e}")

    def _get_audio_download_url(self, speak_v2_url: str, headers: dict) -> str:
        max_wait_time = 10
        retry_interval = 0.5
        elapsed_time = 0

        while elapsed_time < max_wait_time:
            response = requests.get(speak_v2_url, headers=headers)
            response.raise_for_status()

            result = response.json().get("result", {})
            status = result.get("status")

            if status == "done":
                audio_download_url = result.get("audio_download_url")
                if not audio_download_url:
                    raise RuntimeError("Audio download URL is missing in Typecast response.")
                return audio_download_url

            elif status in ["processing", "progress"]:
                time.sleep(retry_interval)
                elapsed_time += retry_interval

            else:
                raise RuntimeError(f"Unexpected status from Typecast API: {status}")

        raise RuntimeError("Audio generation timed out after 10 seconds.")

    def _download_audio(self, audio_download_url: str) -> bytes:
        response = requests.get(audio_download_url, stream=True)
        response.raise_for_status()

        return response.content
