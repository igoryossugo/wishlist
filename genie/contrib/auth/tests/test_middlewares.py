from aiohttp.web import Response

from genie.contrib.auth.middlewares import authorization_middleware


async def test_handler(request):
    return Response(text='I am a handler.')


class TestAuthMiddleware:

    async def test_returns_application_for_authorized_request(
        self,
        make_request,
        application,
        token,
    ):
        request = make_request(
            method='get',
            url='https://www.magazineluiza.com.br/',
            params={'token': token}
        )

        response = await authorization_middleware(
            request=request,
            handler=test_handler
        )

        assert response.status == 200
        assert request.application == application

    async def test_returns_401_for_unauthorized_request(
        self,
        make_request
    ):
        request = make_request(
            method='get',
            url='https://www.magazineluiza.com.br/'
        )

        response = await authorization_middleware(
            request=request,
            handler=test_handler
        )

        assert response.status == 401
