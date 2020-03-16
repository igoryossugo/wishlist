import sqlite3
from ramos.mixins import ThreadSafeCreateMixin

from genie.backends.database.backend import DatabaseBackend


class CacheDatabaseBackend(DatabaseBackend):
    id = 'cache'
    name = 'Cache database'
