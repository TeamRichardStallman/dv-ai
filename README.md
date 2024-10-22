# DV-AI

Interview King Dev Kim AI Repository

## Getting Started

1. 프로젝트 루트에서 아래 명령어를 실행하여 로컬 서버를 시작합니다. (실행 전에 가상 환경을 활성화하고, 필요한 의존성들이 모두 설치되어 있어야 합니다.)

```bash
fastapi dev app/main.py
```

### 의존성 설치

1.  프로젝트 루트에서 가상 환경을 생성합니다.

```bash
python -m venv venv
```

2.  가상 환경을 활성화합니다.

```bash
source venv/bin/activate
```

3.  requirements.txt에 있는 라이브러리를 가상 환경에 설치합니다.

```bash
pip install -r requirements.txt
```

### 의존성 업데이트

1.  가상 환경을 활성화합니다. (가상 환경 venv이 먼저 생성되어 있어야 합니다)

```bash
source venv/bin/activate
```

2.  현재 설치된 라이브러리 목록을 requirements.txt 파일에 업데이트합니다.

```bash
pip freeze > requirements.txt
```
