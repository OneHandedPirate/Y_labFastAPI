import aioredis
from aioredis import Redis

from app.core.settings import REDIS_URL


async def get_redis_connection() -> Redis:
    redis = aioredis.from_url(REDIS_URL)
    async with redis.client() as conn:
        yield conn
