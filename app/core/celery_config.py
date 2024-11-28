from celery import Celery

celery_app = Celery(
    "interview_app",
    broker="redis://ktb-8-dev-redis.cngspe.0001.apn2.cache.amazonaws.com:6379/0",
    backend="redis://ktb-8-dev-redis.cngspe.0001.apn2.cache.amazonaws.com:6379/0",
)

celery_app.conf.task_routes = {
    "app.services.tasks.*": {"queue": "default"},
}
