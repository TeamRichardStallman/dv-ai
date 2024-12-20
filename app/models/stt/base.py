from abc import ABC, abstractmethod


class BaseSTTModel(ABC):
    @abstractmethod
    async def transcribe(self, audio_file: bytes):
        pass
