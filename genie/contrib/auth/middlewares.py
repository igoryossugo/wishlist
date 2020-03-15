import json

from aiohttp import web
from aiohttp.web_exceptions import HTTPError, HTTPUnauthorized

from genie.backends.pools import AuthenticationBackendPool


@web.middleware
async def authorization_middleware(request, handler):
    if (
        hasattr(request, 'match_info') and
        request.match_info.http_exception is not None and
        isinstance(request.match_info.http_exception, HTTPError)
    ):
        return (await handler(request))

    backend = AuthenticationBackendPool.get_default()
    application = backend.authenticate(request=request)

    if not application:
        return HTTPUnauthorized(
            text=json.dumps({'error_message': 'Invalid authentication.'})
        )
    request.application = application

    return (await handler(request))
