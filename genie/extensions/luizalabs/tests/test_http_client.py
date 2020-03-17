from unittest import mock

import pytest
from simple_settings import settings

from genie.extensions.luizalabs.http_client import (
    LuizalabsGetItemHTTPClient,
    LuizalabsHTTPClient
)


class TestLuizalabsHTTPClient:

    @pytest.fixture
    def http_client(self):
        return LuizalabsHTTPClient()

    def test_http_client_has_default_parameters(self, http_client):
        http_client.SUCCESS_STATUS_CODE == {200}
        http_client.base_url = settings.LUIZALABS_SETTINGS['base_url']
        http_client.default_timeout = settings.LUIZALABS_SETTINGS['timeout']

    def test_get_default_headers_returns_header_default(self, http_client):
        http_client.get_default_headers() == {
            'Content-Type': 'application/json'
        }


class TestLuizalabsGetItemHTTPClient:

    @pytest.fixture
    def http_client(self):
        return LuizalabsGetItemHTTPClient()

    async def test_get_item_calls_get(self, http_client):
        with mock.patch.object(http_client, 'get') as mocked_get:
            await http_client.get_item(sku='abc')

        mocked_get.assert_called_with(
            route_url='api/product/abc'
        )
