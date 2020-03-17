from genie.extensions.luizalabs.http_client import LuizalabsGetItemHTTPClient
from genie.tests import vcr_client


class TestLuizalabsHTTPClientIntegration:

    @vcr_client.use_cassette()
    async def test_get_item_integration(self):
        response = await LuizalabsGetItemHTTPClient().get_item(
            sku='82727b28-d6b3-813c-5139-50d3b28c16d4'
        )
        assert response
