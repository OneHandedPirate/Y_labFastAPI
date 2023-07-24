init:
	touch .env
	echo "POSTGRES_USER=postgres\nPOSTGRES_PASSWORD=postgres\nPOSTGRES_DB=postgres\nPOSTGRES_PORT=5432\nPOSTGRES_HOST=localhost" > .env
	poetry install
	poetry shell
up:
	docker compose -f docker-compose-dev.yaml up -d
	sleep 5
	alembic upgrade head
	uvicorn app.main:app --reload
down:
	docker compose -f docker-compose-dev.yaml down