import os

from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter, URLRouter

from .middlewares import JSONWebTokenMiddlewareStack
from .routing import websocket_urlpatterns

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cookbook.settings.local")

websocket_application = JSONWebTokenMiddlewareStack(URLRouter(websocket_urlpatterns))

application = ProtocolTypeRouter(
    {"http": get_asgi_application(), "websocket": websocket_application}
)
