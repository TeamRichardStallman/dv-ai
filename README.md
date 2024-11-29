# DV-AI Interview King Dev Kim AI Repository

## 프로젝트 시작하기

### 사전 준비

1. Poetry 설치

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. 프로젝트 의존성 설치

```bash
poetry shell   # 가상환경 활성화
poetry install # 의존성 설치
```

### 서버 실행

```bash
poetry run fastapi dev app/main.py
# 또는
poetry run uvicorn app.main:app --host 127.0.0.1 --port 8000
```

## 개발 가이드

### 브랜치 전략 (Git-flow)

- `main`: 배포 가능한 안정화된 코드
- `develop`: 개발 중인 통합 브랜치
- `feature/`: 새로운 기능 개발 브랜치
- `release/`: 릴리즈 준비 브랜치
- `hotfix/`: 긴급 버그 수정 브랜치

### 커밋 컨벤션

커밋 메시지 형식: `[Jira 티켓] 타입: 간단한 설명`

#### 커밋 타입

- `feat`: 새로운 기능 추가
- `fix`: 버그 수정
- `refactor`: 코드 리팩토링
- `docs`: 문서 수정
- `style`: 코드 스타일/포맷 변경
- `test`: 테스트 코드 추가/수정
- `chore`: 기타 설정 변경
- `perf`: 성능 개선
- `ci`: CI/CD 설정 변경
- `build`: 빌드 관련 작업

## Poetry 명령어

### 패키지 관리

```bash
# 패키지 추가 (일반)
poetry add python-dotenv

# 개발 의존성 추가
poetry add pytest -D

# 설치된 패키지 확인
poetry show

# 가상환경 정보 확인
poetry env info
```

## 개발 도구

### 린팅 및 포매팅

```bash
poetry run tox -e lint
```

### 테스트 실행

```bash
poetry run pytest app/tests -v
```

### 폴더 구조 생성

```bash
# macOS
brew install tree
tree -I 'wandb|**pycache**|\*.log|__pycache__|folder_structure' > folder_structure.txt
```

## 주의사항

- 가상환경은 항상 `poetry shell`로 활성화
- 의존성은 `pyproject.toml`에서 관리
- 코드 품질을 위해 린팅과 테스트를 주기적으로 실행

### 로컬에서 Celery 워커 실행

```bash
poetry run celery -A app.worker worker --loglevel=info
```

### 로컬에서 redis 실행

```bash
redis-server
```

```bash
docker run -p 6379:6379 --name some-redis -d redis
```

```
docker exec -it some-redis redis-cli
keys *
```
