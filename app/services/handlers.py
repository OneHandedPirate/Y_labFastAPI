import pickle

from fastapi import Depends

from app.repositories.cache import (
    BaseRedisCacheRepository,
    DishCacheRepository,
    MenuCacheRepository,
    SubmenuCacheRepository,
)
from app.repositories.sqlalch import (
    DishRepository,
    MenuRepository,
    SQLAlchemyRepository,
    SubmenuRepository,
)


class BaseService:
    """Base service for endpoints"""

    def __init__(self, repo: SQLAlchemyRepository, cache: BaseRedisCacheRepository):
        self.repo = repo
        self.cache = cache

    async def get(self, *args: int):
        if await self.cache.get_item(*args):
            return pickle.loads(await self.cache.get_item(*args))
        item = await self.repo.get(args[-1])
        await self.cache.set_item(pickle.dumps(item), *args)
        return item

    async def get_list(self, related_model_id=None):
        if related_model_id:
            item_list = list(await self.repo.get_list(related_model_id))
        else:
            item_list = list(await self.repo.get_list())
        return item_list

    async def update(self, _id: int, data: dict):
        await self.cache.update_operation(_id)
        return await self.repo.update(_id, data)

    async def create(self, data: dict, *args: int):
        if args:
            await self.cache.create_operation(*args, entity_name=self.cache.namespace)
        return await self.repo.create(data, args[-1] if args else None)

    async def delete(self, *args: int):
        await self.cache.del_operation(*args, entity_name=self.cache.namespace)
        return await self.repo.delete(args[-1])


class MenuService(BaseService):
    def __init__(self, repo: MenuRepository = Depends(), cache: MenuCacheRepository = Depends()):
        super().__init__(repo, cache)


class SubmenuService(BaseService):
    def __init__(self, repo: SubmenuRepository = Depends(), cache: SubmenuCacheRepository = Depends()):
        super().__init__(repo, cache)


class DishService(BaseService):
    def __init__(self, repo: DishRepository = Depends(), cache: DishCacheRepository = Depends()):
        super().__init__(repo, cache)
