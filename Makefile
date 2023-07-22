up:
	docker compose -f docker-compose-dev.yaml up -d
	sleep 3
	alembic upgrade head
	uvicorn app.main:app --reload
down:
	docker compose -f docker-compose-dev.yaml down