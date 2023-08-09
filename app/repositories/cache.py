from aioredis import Redis
from fastapi import Depends

from app.cache.connection import get_redis_connection
from app.core.settings import CACHE_EXPIRE_TIME


class BaseRedisCacheRepository:
    namespace: str | None = None

    def __init__(self, cache: Redis = Depends(get_redis_connection)) -> None:
        self.cache = cache

    async def get_item(self, *args: int) -> bytes:
        if len(args) == 1:
            to_get = f'menu:{args[0]}'
        elif len(args) == 2:
            to_get = f'menu:{args[0]}:submenu:{args[1]}'
        elif len(args) == 3:
            to_get = f'menu:{args[0]}:submenu:{args[1]}:dish:{args[2]}'
        return await self.cache.get(to_get)

    async def set_item(self, item: bytes, *args: int) -> None:
        if len(args) == 1:
            return await self.cache.set(f'menu:{args[0]}', item, ex=CACHE_EXPIRE_TIME)
        elif len(args) == 2:
            return await self.cache.set(f'menu:{args[0]}:submenu:{args[1]}', item, ex=CACHE_EXPIRE_TIME)
        elif len(args) == 3:
            return await self.cache.set(f'menu:{args[0]}:submenu:{args[1]}:dish:{args[2]}', item, ex=CACHE_EXPIRE_TIME)

    async def update_operation(self, _id: int) -> None:
        key = await self.cache.keys(f'*{self.namespace}:{_id}')
        if key:
            await self.cache.delete(*key)

    async def create_operation(self, *args: int | None, entity_name: str | None = None) -> None:
        if entity_name == 'submenu':
            keys = await self.cache.keys(f'menu:{args[0]}')
        elif entity_name == 'dish':
            keys = await self.cache.keys(f'menu:{args[0]}')
            keys += await self.cache.keys(f'*submenu:{args[1]}')

        if keys:
            await self.cache.delete(*keys)

    async def del_operation(self, *args: int | None, entity_name: str | None = None) -> None:
        if entity_name == 'menu':
            keys = await self.cache.keys(f'menu:{args[0]}*')
        elif entity_name == 'submenu':
            keys = await self.cache.keys(f'*submenu:{args[1]}*')
            keys += await self.cache.keys(f'menu:{args[0]}')

        else:
            keys = await self.cache.keys(f'*submenu:{args[1]}')
            keys += await self.cache.keys(f'menu:{args[0]}')
            keys += await self.cache.keys(f'*dish:{args[2]}')

        if keys:
            await self.cache.delete(*keys)


class MenuCacheRepository(BaseRedisCacheRepository):
    namespace = 'menu'


class SubmenuCacheRepository(BaseRedisCacheRepository):
    namespace = 'submenu'


class DishCacheRepository(BaseRedisCacheRepository):
    namespace = 'dish'
