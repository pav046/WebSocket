# WebSocket Binance Trade

Этот проект представляет собой Django-приложение, которое получает данные о торгах с Binance WebSocket и отправляет их через WebSocket клиентам.

## Функции
- Получение данных о цене BTCUSDT через Binance WebSocket API
- Сохранение данных в базу данных
- Передача данных клиентам через Django Channels

## Стек технологий
- Django + Django REST Framework
- Django Channels
- PostgreSQL
- Pytest

## Установка и запуск

```sh
git clone https://github.com/pav046/WebSocket
cd WebSocket
python -m venv venv
source venv/bin/activate  # для MacOS/Linux
.\venv\Scripts\activate  # для Windows
pip install -r requirements.txt
python manage.py migrate
daphne -b 0.0.0.0 -p 8000 config.asgi:application
```

## Тестирование
```sh
python manage.py test trade
```
