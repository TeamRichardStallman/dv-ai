# Docker Compose 관리용 Makefile

# 기본 타겟
help:
	@echo "Makefile 사용법:"
	@echo "  make build   - Docker Compose 캐시 없이 빌드"
	@echo "  make up      - Docker Compose 실행"
	@echo "  make down    - Docker Compose 중지 및 컨테이너 제거"
	@echo "  make restart - Docker Compose 재시작"
	@echo "  make logs    - 실행 중인 컨테이너의 로그 확인"
	@echo "  make redis-cli   - Docker 컨테이너의 Redis CLI 접속"

# 캐시 없이 빌드
build:
	docker compose build --no-cache

# 컨테이너 실행
up:
	docker compose up --force-recreate

# 컨테이너 중지 및 삭제
down:
	docker compose down

# 재시작
restart: down build up

# 로그 확인
logs:
	docker compose logs -f

# Redis CLI 접속
redis-cli:
	docker exec -it redis redis-cli
