import sys

DEBUG = False

SECOND = 1
MINUTE = 60 * SECOND
HOUR = 60 * MINUTE
DAY = 24 * HOUR

# SIMPLE SETTINGS STUFF
SIMPLE_SETTINGS = {
    'OVERRIDE_BY_ENV': True,
    'CONFIGURE_LOGGING': True
}

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
