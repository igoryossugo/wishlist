import sys

from genie.settings import constants

DEBUG = False

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

# DEFAULT BACKENDS
DEFAULT_AUTHORIZATION_BACKEND = 'static'
DEFAULT_CATALOG_BACKEND = 'fake_success'
DEFAULT_DATABASE_BACKEND = 'sqlite'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(hostname)s %(name)s %(module)s:%(filename)s:%(lineno)d %(process)d %(thread)d == %(message)s'  # noqa
        },
        'simple': {
            'format': '%(hostname)s %(levelname)s %(name)s %(message)s'
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
            'level': 'INFO',
            'propagate': True,
        },
        'gunicorn.access': {
            'level': 'DEBUG',
            'propagate': True
        }
    }
}
