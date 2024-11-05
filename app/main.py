from fastapi import FastAPI
from app.routers import interview
import os
import yaml
from fastapi.openapi.utils import get_openapi
from contextlib import asynccontextmanager

app = FastAPI(
    title="Devterview AI API",
    description="This is the AI API for the Interview King application.",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "Common",
        },
        {
            "name": "Interview",
        },
    ],
)


def generate_openapi_yaml():
    openapi_schema = get_openapi(
        title="Devterview AI API",
        version="1.0.0",
        description="""
        Devterview AI API는 개발자 면접을 위한 질문 생성과 평가를 수행하는 API입니다. 
        이 API는 지원자의 자소서와 면접 데이터를 기반으로 맞춤형 면접 질문을 생성하고, 
        지원자의 답변에 대한 평가를 제공합니다.

        주요 기능:
        - 자소서를 기반으로 한 맞춤형 면접 질문 생성
        - 기술적, 성격적 면접 평가
        - 답변에 대한 세부적인 피드백 제공
        - 사용자 정의 가능한 면접 유형과 직무에 따른 질문 및 평가

        이 API는 다양한 직무(프론트엔드, 백엔드, 클라우드, AI 등)와 다양한 면접 방식(실전 면접, 모의 면접)을 
        지원하며, 기술적인 성장 가능성과 업무 태도에 대한 종합적인 평가를 제공합니다.
        """,
        routes=app.routes,
    )

    os.makedirs("lib", exist_ok=True)

    with open("lib/api-spec.yaml", "w") as file:
        yaml.dump(openapi_schema, file, default_flow_style=False)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    generate_openapi_yaml()


app = FastAPI(lifespan=lifespan)


@app.get("/", tags=["Common"])
async def root():
    return {"message": "Welcome to the Devterview AI Server!"}


app.include_router(interview.router)
