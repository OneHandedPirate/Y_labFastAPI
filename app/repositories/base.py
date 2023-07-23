from abc import ABC, abstractmethod


class BaseCRUDRepository(ABC):
    @abstractmethod
    def get(self, *args):
        pass

    @abstractmethod
    def get_list(self):
        pass

    @abstractmethod
    def create(self, data):
        pass

    @abstractmethod
    def delete(self, *args):
        pass

    @abstractmethod
    def update(self, *args):
        pass
