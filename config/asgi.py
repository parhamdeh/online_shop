import os

from online_shop.users.middleware import JWTAuthMiddleware
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

import online_shop.users.routing

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "online_shop.settings",
)

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": JWTAuthMiddleware(
            URLRouter(
                online_shop.users.routing.websocket_urlpatterns
            )
        ),
    }
)