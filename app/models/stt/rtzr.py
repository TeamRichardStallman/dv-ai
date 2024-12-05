import asyncio
import json

import httpx

from app.core.config import Config

from .base import BaseSTTModel


class RtzrSTTModel(BaseSTTModel):
    def __init__(self):
        self.JWT_TOKEN = None
        self.config = {
            "model_name": "sommers",
            "language": "ko",
            "use_diarization": False,
            "use_itn": True,
            "use_word_timestamp": False,
        }

    async def authenticate(self):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://openapi.vito.ai/v1/authenticate",
                data={
                    "client_id": Config.RTZR_API_CLIENT_ID,
                    "client_secret": Config.RTZR_API_CLIENT_SECRET,
                },
            )
            response.raise_for_status()
            self.JWT_TOKEN = response.json()["access_token"]

    async def transcribe(self, audio_file: bytes) -> str:
        if not self.JWT_TOKEN:
            await self.authenticate()

        headers = {"Authorization": f"Bearer {self.JWT_TOKEN}"}
        files = {"file": ("audio_file.wav", audio_file, "audio/wav")}
        data = {"config": json.dumps(self.config)}

        async with httpx.AsyncClient() as client:
            # Initiate transcription
            response = await client.post(
                "https://openapi.vito.ai/v1/transcribe",
                headers=headers,
                files=files,
                data=data,
            )
            response.raise_for_status()
            test_id = response.json()["id"]

            # Poll for transcription result
            while True:
                resp = await client.get(
                    f"https://openapi.vito.ai/v1/transcribe/{test_id}",
                    headers=headers,
                )
                resp.raise_for_status()
                resp_json = resp.json()
                status = resp_json.get("status")

                if status == "completed":
                    result = resp_json.get("results", {}).get("utterances", [])
                    messages = [utterance.get("msg", "") for utterance in result]
                    text = " ".join(messages)
                    return text
                elif status == "failed":
                    error_message = resp_json.get("message", "Unknown error")
                    raise Exception(f"Transcription failed: {error_message}")
                else:
                    await asyncio.sleep(1)
