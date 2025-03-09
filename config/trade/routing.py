from django.urls import path
from .consumers import TradeConsumer

websocket_urlpatterns = [
    path("ws/trades/", TradeConsumer.as_asgi()),
]