from online_shop.users.routing import websocket_urlpatterns

# یا اگر چند اپ داری

websocket_urlpatterns = [
    *websocket_urlpatterns,
]