from ramos.mixins import DefaultBackendMixin
from ramos.pool import BackendPool


class AuthenticationBackendPool(BackendPool, DefaultBackendMixin):
    SETTINGS_KEY = 'DEFAULT_AUTHORIZATION_BACKEND'
    backend_type = 'authentication'
