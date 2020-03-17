from ramos.mixins import SingletonCreateMixin

from genie.backends.catalog.backend import CatalogBackend
from genie.backends.catalog.exceptions import ItemNotFound
from genie.extensions.fake.factory import fake_item, fake_list_items


class FakeSuccessCatalogBackend(CatalogBackend, SingletonCreateMixin):
    id = 'fake_success'
    name = 'Fake Success Catalog'

    async def _get_item(self, sku):
        return fake_item(sku=sku)

    async def _list_items(self, page=0):
        return fake_list_items()


class FakeErrorCatalogBackend(CatalogBackend, SingletonCreateMixin):
    id = 'fake_error'
    name = 'Fake Error Catalog'

    async def _get_item(self, sku):
        raise ItemNotFound

    async def _list_items(self, page):
        return []
