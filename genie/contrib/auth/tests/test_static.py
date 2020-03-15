import pytest
from simple_settings import settings

from genie.backends.auth.models import Application
from genie.contrib.auth.backends import StaticAuthenticationBackend


class TestStaticAuthentication:

    @pytest.fixture
    def application_name(self):
        return 'dev'

    @pytest.fixture
    def token(self, application_name):
        return settings.AUTH_APPLICATIONS[application_name]

    @pytest.fixture
    def backend(self):
        return StaticAuthenticationBackend.create()

    def test_respects_the_token_from_querystring_param(
        self,
        backend,
        make_request,
        token,
        application_name,
    ):
        request = make_request(
            method='get',
            url='https://genie.luizalabs.com',
            params={'token': token}
        )

        authorized_application = backend.authenticate(request)

        assert isinstance(authorized_application, Application)
        assert application_name == authorized_application.name

    def test_respects_the_token_from_headers(
        self,
        backend,
        make_request,
        token,
        application_name,
    ):
        request = make_request(
            method='get',
            url='https://genie.luizalabs.com',
            headers={backend.AUTH_HEADER: token}
        )

        authorized_application = backend.authenticate(request)

        assert isinstance(authorized_application, Application)
        assert application_name == authorized_application.name

    def test_returns_none_for_non_authenticated_request(
        self,
        backend,
        make_request,
    ):
        request = make_request(
            method='get',
            url='https://genie.luizalabs.com',
        )

        application = backend.authenticate(request)
        assert application is None
