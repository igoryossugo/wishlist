import pytest
from aiohttp.client_reqrep import ClientRequest
from yarl import URL


@pytest.fixture
async def make_request(loop):
    """
    Inspired on aiohttp make-request function
    https://github.com/aio-libs/aiohttp/blob/master/tests/test_client_request.py#L24
    """
    request = None

    def maker(method, url, *args, **kwargs):
        nonlocal request
        request = ClientRequest(method, URL(url), *args, loop=loop, **kwargs)
        return request

    yield maker
    if request is not None:
        await request.close()
