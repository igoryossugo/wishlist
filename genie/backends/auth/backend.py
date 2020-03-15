import abc

from aiohttp.web import Request

from genie.backends.auth.models import Application


class AuthenticationBackend(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def authenticate(
        self,
        request: Request
    ) -> Application:  # pragma: no cover
        pass
