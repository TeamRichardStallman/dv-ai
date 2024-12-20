import app.services.tasks
from app.core.celery_app import celery_app

celery_app.conf.update(
    task_routes={
        "app.services.tasks.*": {"queue": "default"},
    },
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
)

_ = app.services.tasks
