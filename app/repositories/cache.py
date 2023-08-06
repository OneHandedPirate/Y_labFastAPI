from aioredis import Redis
from fastapi import Depends

from app.cache.connection import get_redis_connection
from app.core.settings import CACHE_EXPIRE_TIME


class BaseRedisCacheRepository:
    namespace: str | None = None

    def __init__(self, cache: Redis = Depends(get_redis_connection)):
        self.cache = cache

    async def get_item(self, item_id: int):
        return await self.cache.get(f'{self.namespace}:{item_id}')

    async def get_list(self, related_model_id=None):
        return await self.cache.get(f'{self.namespace}:list:{related_model_id if related_model_id else ""}')

    async def set_item(self, item, item_id: int):
        key = f'{self.namespace}:{item_id}'
        await self.cache.set(key, item, ex=CACHE_EXPIRE_TIME)

    async def set_list(self, items, related_model_id=None):
        key = f'{self.namespace}:list:{related_model_id if related_model_id else ""}'
        await self.cache.set(key, items, ex=CACHE_EXPIRE_TIME)

    async def clear(self):
        await self.cache.flushall()


class MenuCacheRepository(BaseRedisCacheRepository):
    namespace = 'menu'


class SubmenuCacheRepository(BaseRedisCacheRepository):
    namespace = 'submenu'


class DishCacheRepository(BaseRedisCacheRepository):
    namespace = 'dish'
