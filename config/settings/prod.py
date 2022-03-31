from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['localhost','127.0.0.1']

CORS_ORIGIN_WHITELIST = ['http://localhost:3000','http://localhost:8001']

WSGI_APPLICATION = 'config.wsgi.application'

