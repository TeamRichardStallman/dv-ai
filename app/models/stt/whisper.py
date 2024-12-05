import os
import tempfile

from openai import OpenAI

from app.core.config import Config
from app.utils.wpm import calculate_wpm

from .base import BaseSTTModel


class WhisperSTTModel(BaseSTTModel):
    def __init__(self):
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)

    async def transcribe(self, audio_file: bytes) -> str:
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
                temp_file.write(audio_file)
                temp_file_path = temp_file.name

            response = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=open(temp_file_path, "rb"),
                response_format="verbose_json",
                timestamp_granularities=["word"],
            )

            wpm = calculate_wpm(response.to_dict())

            return response.to_dict().get("text"), wpm
        except Exception as e:
            raise RuntimeError(f"Error transcribing audio with OpenAI Whisper API: {e}")
        finally:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)


# 로컬에서 실행해보기 위한 테스트 코드

# if __name__ == "__main__":
#     import asyncio

#     async def main():
#         try:
#             # 실제 오디오 파일 읽기
#             with open("/Users/joon/Documents/KakaoTech_Bootcamp/Team_Project2/dv-ai/temp.wav", "rb") as f:
#                 audio_data = f.read()

#             # 모델 인스턴스 생성
#             model = WhisperSTTModel()

#             # 실제 오디오 데이터를 이용해 transcribe 실행
#             transcription, wpm = await model.transcribe(audio_data)

#             # 결과 출력
#             print("Transcription:", transcription)
#             print("Words Per Minute (WPM):", wpm)
#         except RuntimeError as e:
#             print(f"Error during transcription: {e}")

#     asyncio.run(main())
