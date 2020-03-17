from unittest import mock

import pytest

from genie.extensions.luizalabs.backend import LuizalabsCatalogBackend


class TestLuizalabsCatalogBackend:

    @pytest.fixture
    def backend(self):
        return LuizalabsCatalogBackend()

    async def test_get_item_calls_http_client_and_helper(self, backend):
        with mock.patch(
            'genie.extensions.luizalabs.backend.'
            'LuizalabsGetItemHTTPClient.get_item'
        ) as mocked_client:
            with mock.patch(
                'genie.extensions.luizalabs.backend.build_item_response'
            ) as mocked_helper:
                mocked_client.return_value = {}
                await backend.get_item(sku='abc')

        mocked_client.assert_called_with(sku='abc')
        mocked_helper.assert_called_with({})
