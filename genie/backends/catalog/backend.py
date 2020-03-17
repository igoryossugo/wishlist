import abc
from typing import List

from genie.backends.catalog.models import Item


class CatalogBackend(metaclass=abc.ABCMeta):

    def get_item(self, sku: str) -> Item:
        return self._get_item(sku=sku)

    def list_items(self, page: int = 0) -> List[Item]:
        return self._list_items(page=page)

    @abc.abstractmethod
    def _get_item(self, sku: str):
        pass

    @abc.abstractmethod
    def _list_items(self, page: int):
        pass
