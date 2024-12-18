import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    WANDB_API_KEY = os.getenv("WANDB_API_KEY")

    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_REGION = os.getenv("AWS_REGION")
    S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

    GPT_MODEL = os.getenv("OPENAI_GPT_MODEL")  # other model: gpt-3.5-turbo, gpt-4o
    ANTHROPIC_MODEL = "claude-3-opus-20240229"

    SEED = 456  # 동일한 입력에 대해 일관된 결과를 생성
    TEMPERATURE = 0.78  # 적당히 창의적이고 예측할 수 없는 출력
    TOP_P = 0.8  # 적당히 다양한 단어를 포함, 가능성 높은 후보군을 중심으로 선택

    BACK_API_URL = os.getenv("BACK_API_URL", "http://localhost:8080")

    TYPECAST_API_TOKEN = os.getenv("TYPECAST_API_TOKEN")

    CELERY_BROKER_URL = os.getenv("REDIS_HOST")
    CELERY_RESULT_BACKEND = os.getenv("REDIS_HOST")
