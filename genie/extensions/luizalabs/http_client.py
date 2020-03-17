import logging

from simple_settings import settings

from genie.backends.exceptions import BackendException
from genie.backends.catalog.exceptions import ItemNotFound
from genie.contrib.http_client import BaseHttpClient

logger = logging.getLogger('__name__')


class LuizalabsHTTPClient(BaseHttpClient):

    SUCCESS_STATUS_CODE = {200}
    base_url = settings.LUIZALABS_SETTINGS['base_url']
    default_timeout = settings.LUIZALABS_SETTINGS['timeout']

    def get_default_headers(self):
        return {
            'Content-Type': 'application/json',
        }


class LuizalabsGetItemHTTPClient(LuizalabsHTTPClient):

    async def get_item(self, sku):
        logger.info(f'Get item {sku} from luizalabs API')
        return await self.get(
            route_url=f'api/product/{sku}',
        )

    async def parse_response(self, response):
        if response.status not in self.SUCCESS_STATUS_CODE:
            if response.status == 404:
                raise ItemNotFound

            logger.error(f'Error to get produt. response {response.text()}')
            raise BackendException

        try:
            return await response.json()
        except ValueError:
            logger.error(
                'Error parsing json response from luizalabs. '
                f'Reason: {response.reason} for exception {response.text()}'
            )
            raise BackendException(
                error_message='Error parsing client json response'
            )
