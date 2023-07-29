create_env:
	touch .env
	echo "POSTGRES_USER=postgres\nPOSTGRES_PASSWORD=postgres\nPOSTGRES_DB=postgres\nPOSTGRES_PORT=5432\nPOSTGRES_HOST=db\nPOSTGRES_HOST_TEST=db_test" > .env
up:
	docker compose -f docker-compose-dev.yaml up -d
down:
	docker compose -f docker-compose-dev.yaml down
tests:
	docker compose -f docker-compose-tests.yaml up -d
	docker compose -f docker-compose-tests.yaml logs -f app_test
	docker compose -f docker-compose-tests.yaml down
