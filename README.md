# DV-AI Interview King 개발 리포지토리

## 소개

DV-AI Interview King은 인터뷰 준비 및 평가를 위한 첨단 AI 기반 도구입니다. 이 솔루션은 FastAPI, Celery, Redis, Docker를 활용하여 효율적이고 확장 가능한 인터뷰 평가 시스템을 제공합니다.

## 프로젝트 시작하기

### 사전 준비

#### 1. Poetry 설치

프로젝트 의존성 관리를 위해 Poetry를 사용합니다:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

#### 2. 프로젝트 의존성 설치

```bash
poetry shell  # 가상환경 활성화
poetry install  # 의존성 설치
```

#### 3. 환경 변수 설정

`.env` 파일을 생성하고 다음과 같은 형식으로 환경 변수를 설정하세요:

```env
OPENAI_API_KEY=your_openai_api_key
ELEVENLABS_API_KEY=your_elevenlabs_api_key
ELEVENLABS_VOICE_ID=your_elevenlabs_voice_id
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=your_aws_region
S3_BUCKET_NAME=your_s3_bucket_name
```

## 개발 가이드

### Makefile 사용

프로젝트의 주요 명령어는 Makefile을 통해 간소화되었습니다. 다음 명령어들을 사용할 수 있습니다:

```bash
# 사용 가능한 명령어 목록 확인
make help

# Docker Compose 빌드
make build

# 컨테이너 실행
make up

# 컨테이너 중지 및 삭제
make down

# 컨테이너 재시작
make restart

# 컨테이너 로그 확인
make logs

# Redis CLI 접속
make redis-cli

# 코드 린트 실행
make lint

# 테스트 실행
make test

# 프로젝트 폴더 구조 생성
make tree
```

## CI/CD

GitHub Actions를 사용하여 지속적 통합 및 배포를 자동화합니다. 모든 풀 리퀘스트(PR)는 CI 파이프라인을 통과해야만 병합될 수 있습니다.

## 주요 기능

- **AI 기반 질문 생성**: OpenAI API를 활용하여 맞춤형 인터뷰 질문을 동적으로 생성
- **실시간 평가**: 음성 및 텍스트 답변에 대한 즉각적이고 정밀한 AI 평가
- **심층 결과 분석**: 데이터 기반 인사이트와 구체적인 피드백 제공

## 주의사항

- **환경 변수 관리**: `.env` 파일을 보안과 정확성을 고려하여 신중하게 설정
- **가상환경 활성화**: 모든 개발 및 실행 작업은 `poetry shell`로 가상환경 활성화 후 진행
- **코드 품질 유지**: `make lint` 명령어를 주기적으로 실행하여 코드 표준 준수

## 기여 가이드

1. GitHub Issues에서 새로운 이슈를 생성하거나 기존 이슈 확인
2. `develop` 브랜치에서 새로운 기능 또는 버그 수정을 위한 기능 브랜치 생성
3. 작업 완료 후, 풀 리퀘스트(PR) 생성 및 코드 리뷰 요청

## Makefile 사용 팁

Makefile을 통해 프로젝트 관리를 더욱 효율적으로 수행할 수 있습니다. 자세한 사용법은 `make help` 명령어로 확인하세요.

### 로컬 환경 실행:

```bash
make up ENV_FILE=.env.local
```

### 개발 환경 실행:

```bash
make up ENV_FILE=.env.dev
```

### GitHub Actions 로컬 테스트 (act 도구 필요):

```bash
act --secret-file .secrets
```

## 추가 리소스

- [OpenAI API 문서](https://platform.openai.com/docs/)
- [FastAPI 공식 문서](https://fastapi.tiangolo.com/)
- [Celery 사용 가이드](https://docs.celeryproject.org/)
