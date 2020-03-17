import abc
from typing import List

from genie.backends.catalog.models import Item


class CatalogBackend(metaclass=abc.ABCMeta):

    async def get_item(self, sku: str) -> Item:
        return await self._get_item(sku=sku)

    async def list_items(self, page: int = 0) -> List[Item]:
        return await self._list_items(page=page)

    @abc.abstractmethod
    async def _get_item(self, sku: str):
        pass

    @abc.abstractmethod
    async def _list_items(self, page: int):
        pass
