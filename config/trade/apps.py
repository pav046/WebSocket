from django.apps import AppConfig
import threading

class TradeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'trade'

    def ready(self):
        from trade.binance_ws import start_ws_client
        threading.Thread(target=start_ws_client, daemon=True).start()