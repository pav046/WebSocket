import asyncio
import websockets
import json
from django.utils.timezone import now
from asgiref.sync import sync_to_async, async_to_sync
from channels.layers import get_channel_layer
from trade.models import Trade

BINANCE_WS_URL = "wss://stream.binance.com:9443/ws/btcusdt@trade"

# Время последней отправки
last_sent_time = None
# Интервал отправки сообщений в секундах
SEND_INTERVAL = 30

async def binance_websocket():
    global last_sent_time

    url = BINANCE_WS_URL

    while True:
        try:
            async with websockets.connect(url) as ws:
                while True:
                    message = await ws.recv()
                    if last_sent_time is None or (now() - last_sent_time).seconds >= SEND_INTERVAL:
                        await save_price(message)
                        last_sent_time = now()

        except (websockets.exceptions.ConnectionClosedError, asyncio.TimeoutError) as e:
            print(f"WebSocket разорван: {e}. Переподключение через 5 секунд...")
            await asyncio.sleep(5)

@sync_to_async
def save_price(message):
    data = json.loads(message)
    price = data['p']
    timestamp = now().isoformat()
    trade = Trade(price=price, timestamp=now())
    trade.save()
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "trades",
        {
            "type": "trade_message",
            "message": {"price": price, "timestamp": timestamp},
        }
    )
    return trade


def start_ws_client():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(binance_websocket())
