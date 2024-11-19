# DV-AI

Interview King Dev Kim AI Repository

## Getting Started

1. 프로젝트 루트에서 아래 명령어를 실행하여 로컬 서버를 시작합니다. (실행 전에 가상 환경을 활성화하고, 필요한 의존성들이 모두 설치되어 있어야 합니다.)

```bash
poetry shell # 가상환경 활성화
poetry install # 의존성 설치
```

```bash
poetry run fastapi dev app/main.py
```

### Branch 전략

Git-flow

- main: 배포 가능한 코드
- develop: 개발 진행 중인 코드
- feature: 새로운 기능을 개발하는 브랜치
- release: 릴리즈 준비를 하는 브랜치 (develop -> main 으로 머지할 때 사용)
- hotfix: 긴급 버그 수정을 위한 브랜치 (main에서 분기하는 브랜치)

### Commit Convention

커밋 메시지 구조
[jira ticket] 타입: 간단한 설명

타입

- feat: 새로운 기능 추가
- fix: 버그 수정
- refactor: 코드 리팩토링 (기능 변경 없이 코드 개선)
- docs: 문서 수정 및 업데이트
- style: 코드의 스타일이나 포맷을 수정 (기능에 영향을 주지 않는 변경)
- test: 테스트 추가 또는 수정
- chore: 빌드 시스템, 패키지 매니저 설정 등 기타 잡다한 변경
- perf: 성능 개선
- ci: CI/CD 설정 및 스크립트 변경
- build: 빌드 관련 작업

### Poetry

의존성 설치
`poetry install`

패키지 추가
`poetry add python-dotenv`

dev 패키지 추가
`poetry add pytest -D`

설치된 패키지 확인
`poetry show`

가상환경 활성화
`poetry shell`

가상환경 내에서 명령어 실행
`poetry run fastapi dev app/main.py # in root directory`

# 폴더 구조 txt 파일 생성

```bash
brew install tree # macOS
tree -I 'wandb|**pycache**|\*.log|__pycache__|__init__|folder_structure' > folder_structure.txt
```
