# 베이스 이미지 설정
FROM python:3.10-slim

# 작업 디렉토리 설정
WORKDIR /app

# Poetry 설치
RUN pip install --upgrade pip \
    && pip install poetry

# 의존성 파일 복사 (pyproject.toml, poetry.lock)
COPY pyproject.toml poetry.lock* /app/

# 필요한 라이브러리 설치
RUN poetry install --no-dev --no-root

# 앱 소스 복사
COPY . .

# FastAPI 서버 실행
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
