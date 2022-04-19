from .base import *
import logging

DEBUG = True

ALLOWED_HOSTS = ['*']
CORS_ORIGIN_WHITELIST = ['http://localhost:3000','http://localhost:8001']
CORS_ALLOW_CREDENTIALS = True

# MIDDLEWARE += ('config.middlewares.QueryCountDebugMiddleware',)


l = logging.getLogger('django.bd.backends')
l.setLevel(logging.DEBUG)
l.addHandler(logging.StreamHandler())

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        # 'config.middlewares.QueryCountDebugMiddleware': {
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['console'],
        },
    },
    # 'loggers.middlewares.QueryCountDebugMiddleware': {
    #     'config,': {
    #         'handlers': ['console'],
    #         'level': 'DEBUG',
    #     },
    # },
}

