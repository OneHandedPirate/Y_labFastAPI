create_env:
	touch .env
	echo "POSTGRES_USER=postgres\nPOSTGRES_PASSWORD=postgres\nPOSTGRES_DB=postgres\nPOSTGRES_PORT=5432\nPOSTGRES_HOST=db\nPOSTGRES_HOST_TEST=db_test\nREDIS_HOST=redis\nREDIS_PORT=6379\nRABBIT_USER=guest\nRABBIT_PASSWORD=guest\nRABBIT_HOST=rabbit\nRABBIT_VHOST=vhost" > .env
postman:
	docker compose -f docker-compose-postman.yaml up -d
up:
	docker compose -f docker-compose-dev.yaml up -d
postman_down:
	docker compose -f docker-compose-postman.yaml down
down:
	docker compose -f docker-compose-dev.yaml down
tests:
	docker compose -f docker-compose-tests.yaml up -d
	docker compose -f docker-compose-tests.yaml logs -f app
	docker compose -f docker-compose-tests.yaml down
