from django.urls import path

from online_shop.users.consumer import WalletConsumer

websocket_urlpatterns = [
    path(
        "ws/wallet/",
        WalletConsumer.as_asgi(),
    ),
]