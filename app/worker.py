from app.core.celery_config import celery_app

if __name__ == "__main__":
    celery_app.worker_main(["worker", "--loglevel=info"])
