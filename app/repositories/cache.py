from aioredis import Redis
from fastapi import Depends

from app.cache.connection import get_redis_connection
from app.core.settings import CACHE_EXPIRE_TIME


class BaseRedisCacheRepository:
    namespace: str | None = None

    def __init__(self, cache: Redis = Depends(get_redis_connection)) -> None:
        self.cache = cache

    async def get_item(self, *args: int) -> bytes | None:
        if len(args) == 1:
            to_get = f'menu:{args[0]}'
        elif len(args) == 2:
            to_get = f'menu:{args[0]}:submenu:{args[1]}'
        elif len(args) == 3:
            to_get = f'menu:{args[0]}:submenu:{args[1]}:dish:{args[2]}'
        return await self.cache.get(to_get)

    async def get_list(self, *args: int) -> bytes | None:
        if not args:
            return await self.cache.get('menu:list')
        else:
            if len(args) == 1:
                return await self.cache.get(f'menu:{args[0]}:submenu:list')
            else:
                return await self.cache.get(f'menu:{args[0]}:submenu:{args[1]}:dish:list')

    async def set_list(self, items_list: bytes, *args: int) -> None:
        if not args:
            await self.cache.set('menu:list', items_list, ex=CACHE_EXPIRE_TIME)
        else:
            if len(args) == 1:
                await self.cache.set(f'menu:{args[0]}:submenu:list', items_list,
                                     ex=CACHE_EXPIRE_TIME)
            else:
                await self.cache.set(f'menu:{args[0]}:submenu:{args[1]}:dish:list', items_list,
                                     ex=CACHE_EXPIRE_TIME)

    async def set_item(self, item: bytes, *args: int) -> None:
        if len(args) == 1:
            await self.cache.set(f'menu:{args[0]}', item, ex=CACHE_EXPIRE_TIME)
        elif len(args) == 2:
            await self.cache.set(f'menu:{args[0]}:submenu:{args[1]}', item, ex=CACHE_EXPIRE_TIME)
        elif len(args) == 3:
            await self.cache.set(f'menu:{args[0]}:submenu:{args[1]}:dish:{args[2]}', item,
                                 ex=CACHE_EXPIRE_TIME)

    async def update_operation(self, *args: int) -> None:
        if len(args) == 1:
            keys = await self.cache.keys(f'menu:{args[-1]}')
            keys += await self.cache.keys('menu:list')
        elif len(args) == 2:
            keys = await self.cache.keys(f'*submenu:{args[-1]}')
            keys += await self.cache.keys(f'menu:{args[0]}:submenu:list')
        else:
            keys = await self.cache.keys(f'*dish:{args[-1]}')
            keys += await self.cache.keys(f'menu:{args[0]}:submenu:{args[1]}:dish:list')
        if keys:
            await self.cache.unlink(*keys)

    async def create_operation(self, *args: int | None, entity_name: str | None = None) -> None:
        keys = await self.cache.keys('menu:list')

        if entity_name == 'submenu':
            keys += await self.cache.keys(f'menu:{args[0]}')
            keys += await self.cache.keys(f'menu:{args[0]}:submenu:list')
        elif entity_name == 'dish':
            keys += await self.cache.keys(f'menu:{args[0]}')
            keys += await self.cache.keys(f'*submenu:{args[1]}')
            keys += await self.cache.keys(f'menu:{args[0]}:submenu:{args[1]}:dish:list')
        if keys:
            await self.cache.unlink(*keys)

    async def del_operation(self, *args: int | None, entity_name: str | None = None) -> None:
        if entity_name == 'menu':
            keys = await self.cache.keys(f'menu:{args[0]}*')
        elif entity_name == 'submenu':
            keys = await self.cache.keys(f'*submenu:{args[1]}*')
        else:
            keys = await self.cache.keys(f'*submenu:{args[1]}')
            keys += await self.cache.keys(f'*dish:{args[2]}')
        if entity_name in ('submenu', 'dish'):
            keys += await self.cache.keys(f'menu:{args[0]}')
            keys += await self.cache.keys(f'menu:{args[0]}:submenu:list')
            keys += await self.cache.keys(f'menu:{args[0]}:submenu:{args[1]}:dish:list')

        keys += await self.cache.keys('menu:list')

        if keys:
            await self.cache.unlink(*keys)


class MenuCacheRepositoryBase(BaseRedisCacheRepository):
    namespace = 'menu'


class SubmenuCacheRepositoryBase(BaseRedisCacheRepository):
    namespace = 'submenu'


class DishCacheRepositoryBase(BaseRedisCacheRepository):
    namespace = 'dish'
