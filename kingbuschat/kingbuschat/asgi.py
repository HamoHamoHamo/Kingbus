"""
ASGI config for kingbuschat project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kingbuschat.settings')
django.setup()
# https://stdworkflow.com/38/daphne-django-core-exceptions-improperlyconfigured-requested-setting-installed-apps-but-settings

from channels.auth import AuthMiddlewareStack
# from .channelsmiddleware import TokenAuthMiddleware
from channels.routing import ProtocolTypeRouter, URLRouter

from django.core.asgi import get_asgi_application
from chat import routing as chatrouting



application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    # "websocket": TokenAuthMiddleware(AuthMiddlewareStack
    "websocket": AuthMiddlewareStack(
        URLRouter(chatrouting.websocket_urlpatterns)
    )
})

