from ramos.mixins import SingletonCreateMixin
from simple_settings import settings

from genie.backends.auth.backend import AuthenticationBackend
from genie.backends.auth.models import Application


class StaticAuthenticationBackend(SingletonCreateMixin, AuthenticationBackend):
    id = 'static'
    name = 'Static Authentication'

    AUTH_HEADER = 'Authorization'

    def authenticate(self, request):
        token = self._get_token(request)

        if not token:
            return

        for name, application_token in settings.AUTH_APPLICATIONS.items():
            if application_token == token:
                return Application(name=name, active=True)

    def _get_token(self, request):
        if 'token' in request.url.query:
            return request.url.query['token']
        elif self.AUTH_HEADER in request.headers:
            return request.headers[self.AUTH_HEADER]
