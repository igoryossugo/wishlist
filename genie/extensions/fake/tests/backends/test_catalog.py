import pytest

from genie.backends.catalog.exceptions import ItemNotFound
from genie.backends.catalog.models import Item
from genie.extensions.fake.backends.catalog import (
    FakeErrorCatalogBackend,
    FakeSuccessCatalogBackend
)


class TestFakeSuccessCatalogBackend:

    @pytest.fixture
    def backend(self):
        return FakeSuccessCatalogBackend()

    def test_get_item_returns_item(self, backend):
        item = backend.get_item(sku='eaefc867-10a6-3a5e-947d-43a984964fcf')
        assert isinstance(item, Item)
        assert item.sku == 'eaefc867-10a6-3a5e-947d-43a984964fcf'

    def test_list_items_returns_list_of_item(self, backend):
        items = backend.list_items()
        assert isinstance(items, list)
        assert isinstance(items[0], Item)


class TestFakeErrorCatalogBackend:

    @pytest.fixture
    def backend(self):
        return FakeErrorCatalogBackend()

    def test_get_items_should_raise_exception(self, backend):
        with pytest.raises(ItemNotFound):
            backend.get_item(sku='a')

    def test_list_items_returns_empty_list(self, backend):
        assert backend.list_items() == []
