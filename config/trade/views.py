from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .models import Trade
from .serializers import TradeSerializer


def index(request):
    return render(request, 'trade/index.html')

class TradeHistoryAPIView(ListAPIView):
    """API-представление для получения истории цен"""
    queryset = Trade.objects.all().order_by('-timestamp')
    serializer_class = TradeSerializer
