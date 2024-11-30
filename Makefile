# Docker Compose 관리용 Makefile

# 기본 명령어 목록
help:
	@echo "Makefile 사용법:"
	@echo "  make build      - Docker Compose 캐시 없이 빌드"
	@echo "  make up         - Docker Compose 컨테이너 실행"
	@echo "  make down       - Docker Compose 컨테이너 중지 및 삭제"
	@echo "  make restart    - Docker Compose 컨테이너 재시작"
	@echo "  make logs       - 실행 중인 컨테이너 로그 확인"
	@echo "  make redis-cli  - Redis CLI 접속"
	@echo "  make lint       - 코드 린트 실행"
	@echo "  make test       - Docker 환경에서 테스트 실행"
	@echo "  make tree       - 폴더 구조를 tree 명령어로 파일로 저장"

# Docker Compose 캐시 없이 빌드
build:
	docker compose build --no-cache

ENV_FILE ?= .env.local

# Docker Compose 컨테이너 실행
up:
	ENV_FILE=$(ENV_FILE) docker compose --env-file $(ENV_FILE) up --build --force-recreate

# Docker Compose 컨테이너 중지 및 삭제
down:
	docker compose down --timeout 10 --volumes || docker ps -q | xargs -r docker rm -f

# Docker Compose 컨테이너 재시작
restart: down build up

# 실행 중인 컨테이너의 로그 확인
logs:
	docker compose logs -f

# Redis CLI 접속
redis-cli:
	docker exec -it redis redis-cli

# 코드 린트 실행
lint:
	poetry run tox -e lint

# Docker Compose 테스트 실행
test:
	docker compose -f docker-compose.test.yml up --build --abort-on-container-exit

# 폴더 구조를 tree 명령어로 파일로 저장
# - 'wandb', '__pycache__', '*.log', 'folder_structure'와 같은 폴더 및 파일 제외
# - 결과는 folder_structure.txt 파일로 저장
tree:
	tree -I 'wandb|**pycache**|\*.log|__pycache__|folder_structure' > folder_structure.txt
