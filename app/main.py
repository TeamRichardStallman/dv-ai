from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from app.core.middleware import add_cors_middleware
from app.routers import interview, task
from app.utils.init import lifespan

description = """
**Devterview AI API**는 개발자 면접을 위한 질문 생성과 평가를 수행하는 API입니다.
이 API는 지원자의 자소서와 면접 데이터를 기반으로 맞춤형 면접 질문을 생성하고,
지원자의 답변에 대한 평가를 제공합니다.
"""

app = FastAPI(
    title="Devterview AI API",
    version="1.0.0",
    description=description,
    openapi_tags=[
        {"name": "Common"},
        {"name": "Task"},
        {"name": "Interview"},
    ],
    lifespan=lifespan,
)


add_cors_middleware(app)


Instrumentator().instrument(app).expose(app, include_in_schema=False)


@app.get("/", tags=["Common"])
async def ping():
    return {"message": "Welcome to the Devterview AI Server!"}


app.include_router(task.router)
app.include_router(interview.router)
