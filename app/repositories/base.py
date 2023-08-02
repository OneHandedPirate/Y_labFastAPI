from abc import ABC, abstractmethod


class BaseCRUDRepository(ABC):
    """Base repository for async CRUD operations"""

    @abstractmethod
    async def get(self, *args):
        pass

    @abstractmethod
    async def get_list(self):
        pass

    @abstractmethod
    async def create(self, data):
        pass

    @abstractmethod
    async def delete(self, *args):
        pass

    @abstractmethod
    async def update(self, *args):
        pass
