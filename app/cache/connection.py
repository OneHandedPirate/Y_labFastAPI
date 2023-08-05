import aioredis

from settings import REDIS_URL


async def get_redis_connection():
    redis = aioredis.from_url(REDIS_URL)
    async with redis.client() as conn:
        yield conn
