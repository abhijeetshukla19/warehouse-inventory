from django.db.models import Sum, F, Case, When
from .models import StockDetail

def get_product_stock(product_id):
    stock_data = StockDetail.objects.filter(product_id=product_id) \
        .annotate(adj_qty=Case(
            When(transaction__transaction_type='IN', then=F('quantity')),
            When(transaction__transaction_type='OUT', then=-F('quantity'))
        )).aggregate(total_qty=Sum('adj_qty'))
    return stock_data['total_qty'] or 0

def get_inventory(as_of_date):
    stock = StockDetail.objects.filter(transaction__date__lte=as_of_date) \
        .annotate(adj_qty=Case(
            When(transaction__transaction_type='IN', then=F('quantity')),
            When(transaction__transaction_type='OUT', then=-F('quantity'))
        )).values('product__code', 'product__name') \
        .annotate(total_qty=Sum('adj_qty'))
    return list(stock)
