import io

from google.cloud import texttospeech

from .base import BaseTTSModel


class GoogleTTSModel(BaseTTSModel):
    def __init__(self):
        self.client = texttospeech.TextToSpeechClient()

    async def synthesize(self, text: str, name: str = "ko-KR-Wavenet-C") -> bytes:
        try:
            synthesis_input = texttospeech.SynthesisInput(text=text)

            voice = texttospeech.VoiceSelectionParams(language_code="ko-KR", name=name)

            audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

            response = self.client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

            audio_stream = io.BytesIO()
            audio_stream.write(response.audio_content)
            audio_stream.seek(0)

            return audio_stream.read()
        except Exception as e:
            raise RuntimeError(f"Error synthesizing audio with Google TTS: {e}")
