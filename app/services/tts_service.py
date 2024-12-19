from .tts_factory import get_tts_model


class TTSService:
    def __init__(self, model_name: str):
        self.tts_model = get_tts_model(model_name)

    async def generate_speech(self, text: str) -> str:
        return await self.tts_model.synthesize(text)


def get_tts_service(model_name: str = "elevenlabs"):
    return TTSService(model_name=model_name)
