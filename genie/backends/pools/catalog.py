from ramos.mixins import DefaultBackendMixin
from ramos.pool import BackendPool


class CatalogBackendPool(BackendPool, DefaultBackendMixin):
    SETTINGS_KEY = 'DEFAULT_CATALOG_BACKEND'
    backend_type = 'catalog'
