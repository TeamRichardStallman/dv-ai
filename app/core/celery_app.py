from celery import Celery

celery_app = Celery(
    "interview_app",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0",
)
