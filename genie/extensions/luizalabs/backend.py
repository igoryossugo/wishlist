from typing import List

from ramos.mixins import ThreadSafeCreateMixin

from genie.backends.catalog.backend import CatalogBackend
from genie.backends.catalog.models import Item
from genie.extensions.luizalabs.helpers import build_item_response
from genie.extensions.luizalabs.http_client import LuizalabsGetItemHTTPClient


class LuizalabsCatalogBackend(CatalogBackend, ThreadSafeCreateMixin):
    id = 'luizalabs'
    name = 'Luizalabs'

    async def _get_item(self, sku: str) -> Item:
        response = await LuizalabsGetItemHTTPClient().get_item(sku=sku)
        return build_item_response(response)

    async def _list_items(self, sku: str) -> List[Item]:
        pass
