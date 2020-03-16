import abc
from typing import List

from genie.backends.catalog.models import Item


class CatalogBackend(metaclass=abc.ABCMeta):

    def get_item(self, sku: str) -> Item:
        return self._get_item(self, sku)

    def list(self, page: int = 0) -> List[Item]:
        return self._list(page=page)

    @abc.abstractmethod
    def _get_item(self, sku: str):
        pass

    @abc.abstractmethod
    def _list(self, page: int):
        pass
