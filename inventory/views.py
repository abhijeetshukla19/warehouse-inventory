from datetime import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import StockDetail
from .serializers import StockDetailSerializer

@api_view(['GET'])
def inventory_report(request):
    date_str = request.GET.get('date')
    if date_str:
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
            details = StockDetail.objects.filter(transaction__date__date=date_obj)
        except ValueError:
            details = StockDetail.objects.none()
    else:
        details = StockDetail.objects.all()

    serializer = StockDetailSerializer(details, many=True)
    return Response(serializer.data)
from rest_framework import viewsets
from .models import Product, StockTransaction
from .serializers import ProductSerializer, StockTransactionSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class StockTransactionViewSet(viewsets.ModelViewSet):
    queryset = StockTransaction.objects.all()
    serializer_class = StockTransactionSerializer

from django.shortcuts import render

def home(request):
    return render(request, "inventory/home.html")
