import pickle

from fastapi import Depends

from app.repositories.cache import (
    DishCacheRepository,
    MenuCacheRepository,
    SubmenuCacheRepository
)
from app.repositories.sqlalch import DishRepository, MenuRepository, SubmenuRepository

# class MenuService:
#     def __init__(self, repo: MenuRepository = Depends(),
#                  cache: MenuCacheRepository = Depends()):
#         self.repo = repo
#         self.cache = cache
#
#     async def get(self, _id: int):
#         if await self.cache.get_item(_id):
#             return pickle.loads(await self.cache.get_item(_id))
#         menu = await self.repo.get(_id)
#         await self.cache.set_item(pickle.dumps(menu), _id)
#
#         return menu
#
#     async def get_list(self):
#         from_cache = await self.cache.get_list()
#         if from_cache:
#             return pickle.loads(from_cache)
#         menu_list = list(await self.repo.get_list())
#         await self.cache.set_list(pickle.dumps(menu_list))
#         return menu_list
#
#     async def update(self, _id, data):
#         await self.cache.clear()
#         return await self.repo.update(_id, data)
#
#     async def create(self, menu):
#         await self.cache.clear()
#         return await self.repo.create(menu)
#
#     async def delete(self, _id):
#         await self.cache.clear()
#         return await self.repo.delete(_id)
#
#
# class SubmenuService:
#     def __init__(self, repo: SubmenuRepository = Depends(),
#                  cache: SubmenuCacheRepository = Depends()):
#         self.repo = repo
#         self.cache = cache
#
#     async def get(self, _id: int):
#         if await self.cache.get_item(_id):
#             return pickle.loads(await self.cache.get_item(_id))
#         menu = await self.repo.get(_id)
#         await self.cache.set_item(pickle.dumps(menu), _id)
#
#         return menu
#
#     async def get_list(self, related_model_id: int):
#         from_cache = await self.cache.get_list(related_model_id)
#         if from_cache:
#             return pickle.loads(from_cache)
#         menu_list = list(await self.repo.get_list(related_model_id))
#         await self.cache.set_list(pickle.dumps(menu_list), related_model_id)
#         return menu_list
#
#     async def update(self, _id: int, data):
#         await self.cache.clear()
#         return await self.repo.update(_id, data)
#
#     async def create(self, data, related_model_id: int):
#         await self.cache.clear()
#         return await self.repo.create(data, related_model_id)
#
#     async def delete(self, _id):
#         await self.cache.clear()
#         return await self.repo.delete(_id)
#
#
# class DishService:
#     def __init__(self, repo: DishRepository = Depends(),
#                  cache: DishCacheRepository = Depends()):
#         self.repo = repo
#         self.cache = cache
#
#     async def get(self, _id: int):
#         if await self.cache.get_item(_id):
#             return pickle.loads(await self.cache.get_item(_id))
#         menu = await self.repo.get(_id)
#         await self.cache.set_item(pickle.dumps(menu), _id)
#
#         return menu
#
#     async def get_list(self, related_model_id: int):
#         from_cache = await self.cache.get_list(related_model_id)
#         if from_cache:
#             return pickle.loads(from_cache)
#         menu_list = list(await self.repo.get_list(related_model_id))
#         await self.cache.set_list(pickle.dumps(menu_list), related_model_id)
#         return menu_list
#
#     async def update(self, _id: int, data):
#         await self.cache.clear()
#         return await self.repo.update(_id, data)
#
#     async def create(self, data, related_model_id: int):
#         await self.cache.clear()
#         return await self.repo.create(data, related_model_id)
#
#     async def delete(self, _id: int):
#         await self.cache.clear()
#         return await self.repo.delete(_id)


class BaseService:
    """Base service for endpoints"""

    def __init__(self, repo, cache):
        self.repo = repo
        self.cache = cache

    async def get(self, _id: int):
        if await self.cache.get_item(_id):
            return pickle.loads(await self.cache.get_item(_id))
        item = await self.repo.get(_id)
        await self.cache.set_item(pickle.dumps(item), _id)
        return item

    async def get_list(self, related_model_id=None):
        if related_model_id:
            from_cache = await self.cache.get_list(related_model_id)
            if from_cache:
                return pickle.loads(from_cache)
            item_list = list(await self.repo.get_list(related_model_id))
            await self.cache.set_list(pickle.dumps(item_list), related_model_id)
            return item_list
        else:
            from_cache = await self.cache.get_list()
            if from_cache:
                return pickle.loads(from_cache)
            item_list = list(await self.repo.get_list())
            await self.cache.set_list(pickle.dumps(item_list))
            return item_list

    async def update(self, _id: int, data):
        await self.cache.clear()
        return await self.repo.update(_id, data)

    async def create(self, data, related_model_id=None):
        await self.cache.clear()
        return await self.repo.create(data, related_model_id)

    async def delete(self, _id: int):
        await self.cache.clear()
        return await self.repo.delete(_id)


class MenuService(BaseService):
    def __init__(self, repo: MenuRepository = Depends(), cache: MenuCacheRepository = Depends()):
        super().__init__(repo, cache)


class SubmenuService(BaseService):
    def __init__(self, repo: SubmenuRepository = Depends(), cache: SubmenuCacheRepository = Depends()):
        super().__init__(repo, cache)


class DishService(BaseService):
    def __init__(self, repo: DishRepository = Depends(), cache: DishCacheRepository = Depends()):
        super().__init__(repo, cache)
