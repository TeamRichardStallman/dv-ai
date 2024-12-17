import os
import uuid
from io import BytesIO
from typing import Dict, List

import fitz
import yaml
from docx import Document
from fastapi.openapi.utils import get_openapi


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


def create_file_objects(file_paths: List[str]) -> List[Dict[str, str]]:
    file_objects = []

    for file_path in file_paths:
        file_type = file_path.split("/")[0]
        file_objects.append({"type": file_type, "path": file_path})

    return file_objects


def process_pdf(file_data: bytes) -> str:
    try:
        temp_pdf_path = "temp.pdf"
        with open(temp_pdf_path, "wb") as temp_pdf_file:
            temp_pdf_file.write(file_data)

        doc = fitz.open(temp_pdf_path)
        texts = []
        for page in doc:
            text = page.get_text("text")
            if text:
                texts.append(text.strip())
        doc.close()

        return "\n".join(texts)
    except Exception as e:
        print(f"Error processing PDF: {e}")
        return ""


def process_txt(file_data: bytes) -> str:
    try:
        text = file_data.decode("utf-8", errors="ignore")
        return text.strip()
    except Exception as e:
        print(f"Error processing TXT: {e}")
        return ""


def process_docx(file_data: bytes) -> str:
    try:
        temp_file = BytesIO(file_data)
        doc = Document(temp_file)
        texts = [paragraph.text for paragraph in doc.paragraphs if paragraph.text.strip()]
        return "\n".join(texts)
    except Exception as e:
        print(f"Error processing DOCX: {e}")
        return ""


def process_file(file_data: List[Dict[str, str]]) -> str:
    file_path = file_data[0]["path"]
    file_data = file_data[0]["data"]

    _, ext = os.path.splitext(file_path.lower())

    if ext == ".pdf" or ext == ".pptx":
        return process_pdf(file_data)
    elif ext == ".txt":
        return process_txt(file_data)
    elif ext == ".docx":
        return process_docx(file_data)
    else:
        print(f"Unsupported file type: {ext}")
        return ""


def generate_uuid() -> str:
    return str(uuid.uuid4())


def ensure_feedback_fields(data: dict) -> dict:
    if "feedback" not in data["answer"] or not isinstance(data["answer"]["feedback"], dict):
        data["answer"]["feedback"] = {"strengths": "N/A", "improvement": "N/A", "suggestion": "N/A"}
    return data
