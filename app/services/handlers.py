import pickle

from fastapi import BackgroundTasks, Depends

from app.repositories.cache import (
    BaseRedisCacheRepository,
    DishCacheRepositoryBase,
    MenuCacheRepositoryBase,
    SubmenuCacheRepositoryBase,
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
        item_from_cache = await self.cache.get_item(*args)
        if item_from_cache:
            return pickle.loads(item_from_cache)
        item = await self.repo.get(args[-1])
        await self.cache.set_item(pickle.dumps(item), *args)
        return item

    async def get_list(self, *args: int):
        if args:
            list_from_cache: bytes | None = await self.cache.get_list(*args)
            if list_from_cache:
                return pickle.loads(list_from_cache)
            item_list = list(await self.repo.get_list(args[-1]))
            await self.cache.set_list(pickle.dumps(item_list), *args)
        else:
            list_from_cache = await self.cache.get_list()
            if list_from_cache:
                return pickle.loads(list_from_cache)
            item_list = list(await self.repo.get_list())
            await self.cache.set_list(pickle.dumps(item_list))
        return item_list

    async def update(self, data: dict, *args: int, bg_tasks: BackgroundTasks):
        bg_tasks.add_task(self.cache.update_operation, *args)
        return await self.repo.update(args[-1], data)

    async def create(self, data: dict, *args: int, bg_tasks: BackgroundTasks):
        if args:
            bg_tasks.add_task(self.cache.create_operation, *args, entity_name=self.cache.namespace)
        else:
            bg_tasks.add_task(self.cache.create_operation, entity_name=self.cache.namespace)
        return await self.repo.create(data, args[-1] if args else None)

    async def delete(self, *args: int, bg_tasks: BackgroundTasks):
        bg_tasks.add_task(self.cache.del_operation, *args, entity_name=self.cache.namespace)
        return await self.repo.delete(args[-1])


class MenuService(BaseService):
    def __init__(self, repo: MenuRepository = Depends(), cache: MenuCacheRepositoryBase = Depends()):
        super().__init__(repo, cache)

    async def get_all(self):
        from_cache = await self.cache.get_item()
        if from_cache:
            return pickle.loads(from_cache)
        _all = list(await self.repo.get_all())
        await self.cache.set_all(pickle.dumps(_all))
        return _all


class SubmenuService(BaseService):
    def __init__(self, repo: SubmenuRepository = Depends(), cache: SubmenuCacheRepositoryBase = Depends()):
        super().__init__(repo, cache)


class DishService(BaseService):
    def __init__(self, repo: DishRepository = Depends(), cache: DishCacheRepositoryBase = Depends()):
        super().__init__(repo, cache)
