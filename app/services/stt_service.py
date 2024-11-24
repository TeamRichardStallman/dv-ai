from .stt_factory import get_stt_model


class STTService:
    def __init__(self, model_name: str):
        self.stt_model = get_stt_model(model_name)

    async def transcribe_audio(self, audio_file: bytes) -> str:
        return await self.stt_model.transcribe(audio_file)


def get_stt_service(model_name: str = "whisper"):
    return STTService(model_name=model_name)
