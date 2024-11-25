import io

from google.cloud import speech
from pydub import AudioSegment

from .base import BaseSTTModel


class GoogleSTTModel(BaseSTTModel):
    def __init__(self):
        self.client = speech.SpeechClient()

    async def transcribe(self, audio_file: bytes, language_code: str = "ko-KR") -> str:
        try:
            audio = AudioSegment.from_file(io.BytesIO(audio_file), format="mp3")
            flac_audio = io.BytesIO()
            audio.export(flac_audio, format="flac")
            flac_audio.seek(0)

            audio_data = speech.RecognitionAudio(content=flac_audio.read())

            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
                sample_rate_hertz=audio.frame_rate,
                language_code=language_code,
                enable_word_time_offsets=True,
                enable_automatic_punctuation=True,
            )

            response = self.client.recognize(config=config, audio=audio_data)

            transcript = " ".join([result.alternatives[0].transcript for result in response.results])
            return transcript

        except Exception as e:
            raise RuntimeError(f"Error transcribing audio with Google STT: {e}")
