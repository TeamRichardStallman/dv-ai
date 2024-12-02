from celery import Celery

from app.core.config import Config

celery_app = Celery(
    "interview_app",
    broker=Config.CELERY_BROKER_URL,
    backend=Config.CELERY_RESULT_BACKEND,
)
