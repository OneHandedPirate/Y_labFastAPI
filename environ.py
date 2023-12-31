import os

from dotenv import load_dotenv

load_dotenv()


POSTGRES_USER: str | None = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD: str | None = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB: str | None = os.getenv('POSTGRES_DB')
POSTGRES_PORT: str | None = os.getenv('POSTGRES_PORT')
POSTGRES_HOST: str | None = os.getenv('POSTGRES_HOST')

REDIS_HOST: str | None = os.getenv('REDIS_HOST')
REDIS_PORT: str | None = os.getenv('REDIS_PORT')

RABBIT_USER: str | None = os.getenv('RABBIT_USER')
RABBIT_PASSWORD: str | None = os.getenv('RABBIT_PASSWORD')
RABBIT_HOST: str | None = os.getenv('RABBIT_HOST')
RABBIT_VHOST: str | None = os.getenv('RABBIT_VHOST')
