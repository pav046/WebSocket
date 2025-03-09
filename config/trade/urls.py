from django.urls import path
from .views import TradeHistoryAPIView, index

urlpatterns = [
    path('', index, name='index'),
    path('api/history/', TradeHistoryAPIView.as_view(), name='trade-history'),
]
