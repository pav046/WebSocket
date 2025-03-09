import json
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from channels.testing import WebsocketCommunicator
from trade.models import Trade
from config.asgi import application

class TradeModelTest(TestCase):
    """Тесты для модели Trade"""

    def test_create_trade(self):
        """Проверяем, что можно создать запись в БД"""
        trade = Trade.objects.create(price=50000.1234)
        self.assertEqual(trade.price, 50000.1234)
        self.assertIsNotNone(trade.timestamp)

class TradeHistoryAPITest(APITestCase):
    """Тесты для REST API истории торгов"""

    def setUp(self):
        """Создаем тестовые данные"""
        Trade.objects.create(price=50000.1234)
        Trade.objects.create(price=51000.5678)

    def test_get_trade_history(self):
        """Проверяем, что API возвращает историю торгов"""
        url = reverse('trade-history')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertIn("price", response.data[0])

class BinanceWebSocketTest(TestCase):
    """Тест обработки данных из Binance WebSocket"""

    def test_binance_message_parsing(self):
        """Проверяем, что входящие сообщения Binance корректно парсятся"""
        from trade.binance_ws import save_price

        sample_message = json.dumps({
            "s": "BTCUSDT",
            "p": '52000.45'
        })

        trade = async_to_sync(save_price)(sample_message)
        self.assertEqual(trade.price, '52000.45')


class WebSocketServerTest(TestCase):
    """Тесты для WebSocket-соединения"""

    async def test_websocket_connection(self):
        """Проверяем, что WebSocket-соединение устанавливается и сервер отправляет данные"""

        communicator = WebsocketCommunicator(application, "/ws/trades/")
        connected, _ = await communicator.connect()
        self.assertTrue(connected)

        test_message = {"price": "51000.5678", "timestamp": "2025-03-09T19:27:31.904308Z"}
        channel_layer = get_channel_layer()
        await channel_layer.group_send("trades", {"type": "trade_message", "message": test_message})

        response = await communicator.receive_json_from()
        self.assertEqual(response, test_message)
        await communicator.disconnect()
