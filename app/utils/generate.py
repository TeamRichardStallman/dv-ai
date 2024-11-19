import os
from typing import List

import yaml
from fastapi.openapi.utils import get_openapi

from app.utils.s3 import get_s3_object


def generate_file_objects(file_paths: List[str]):
    new_file_paths = []
    for path in file_paths:
        new_file_paths.extend(path.split(","))

    file_objects = []
    for path in new_file_paths:
        parts = path.split("/", 1)
        if len(parts) == 2:
            type_ = parts[0][:-1]
            file_path = path
        else:
            type_, file_path = "unknown", path
        file_objects.append({"type": type_, "file_path": file_path})

    return file_objects


async def generate_file_data(file_objects):
    file_data = []

    for object in file_objects:
        data = await get_s3_object(object["file_path"])
        file_data.append({"type": object["type"], "data": data})

    return file_data


def generate_openapi_yaml(app):
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
