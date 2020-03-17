from typing import List

from ramos.mixins import ThreadSafeCreateMixin

from genie.backends.catalog.backend import CatalogBackend
from genie.backends.catalog.models import Item


class LuizalabsCatalogBackend(CatalogBackend, ThreadSafeCreateMixin):
    id = 'luizalabs'
    name = 'Luizalabs'

    def _get_item(self, sku: str) -> Item:
        pass

    def _list_items(self, sku: str) -> List[Item]:
        pass
