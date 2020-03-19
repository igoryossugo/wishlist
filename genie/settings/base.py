import os
import sys

from genie.settings import constants

DEBUG = False

BASE_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..')

# SIMPLE SETTINGS STUFF
SIMPLE_SETTINGS = {
    'OVERRIDE_BY_ENV': True,
    'CONFIGURE_LOGGING': True
}

POOL_OF_RAMOS = {
    'authentication': [
        constants.STATIC_AUTHORIZATION_BACKEND,
    ],
    'catalog': [
        constants.FAKE_SUCCESS_CATALOG_BACKEND,
        constants.FAKE_ERROR_CATALOG_BACKEND,
    ],
    'database': [
        constants.SQLITE_DATABASE_BACKEND,
    ],
}

# Auth applications
AUTH_APPLICATIONS = {
    'dev': 'jovem'
}

DATABASE = {
    'NAME': os.environ.get('MYSQL_DATABASE_NAME', 'genie'),
    'USER': os.environ.get('MYSQL_USER', 'root'),
    'PASSWORD': os.environ.get('MYSQL_PASSWORD', ''),
    'HOST': os.environ.get('MYSQL_HOST', '127.0.0.1'),
    'PORT': os.environ.get('MYSQL_PORT', '3306'),
    'CONN_MAX_AGE': int(os.environ.get(
        'MYSQL_CONN_MAX_AGE',
        4 * constants.HOURS
    )),
}


# DEFAULT BACKENDS
DEFAULT_AUTHORIZATION_BACKEND = 'static'
DEFAULT_CATALOG_BACKEND = 'fake_success'
DEFAULT_DATABASE_BACKEND = 'mysql'


# EXTENSIONS SETTINGS
# LUIZALABS SETTINGS
LUIZALABS_SETTINGS = {
    'base_url': 'http://challenge-api.luizalabs.com',
    'timeout': 2,
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(name)s %(module)s:%(filename)s:%(lineno)d %(process)d %(thread)d == %(message)s'  # noqa
        },
        'simple': {
            'format': '%(levelname)s %(name)s %(message)s'
        },
    },
    'handlers': {
        'stdout': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'simple',
        },
    },
    'loggers': {
        '': {
            'handlers': ['stdout'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'genie': {
            'handlers': ['stdout'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'gunicorn.access': {
            'level': 'DEBUG',
            'propagate': True
        }
    }
}

# REDIS
REDIS_DB = 1
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_POOLSIZE = 4
MATCHER_CACHE_TTL = 60 * 30

CACHE = {
    'default': {
        'cache': 'aiocache.RedisCache',
        'endpoint': REDIS_HOST,
        'port': int(REDIS_PORT),
        'db': REDIS_DB,
        'pool_max_size': REDIS_POOLSIZE,
        'timeout': 1,
        'serializer': {
            'class': 'aiocache.serializers.JsonSerializer'
        },
    }
}


WISHLIST_CACHE_MAX_AGE = 10 * constants.MINUTES
