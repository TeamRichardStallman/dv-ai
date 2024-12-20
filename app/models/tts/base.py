from abc import ABC, abstractmethod


class BaseTTSModel(ABC):
    @abstractmethod
    async def synthesize(self, text: str, language_code: str = "ko") -> bytes:
        pass
