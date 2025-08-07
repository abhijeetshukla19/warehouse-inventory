from django.db import models
from django.core.exceptions import ValidationError

class Product(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code} - {self.name}"


class StockTransaction(models.Model):
    TRANSACTION_TYPES = [
        ('IN', 'Stock In'),
        ('OUT', 'Stock Out')
    ]
    date = models.DateTimeField()
    transaction_type = models.CharField(max_length=3, choices=TRANSACTION_TYPES)
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} on {self.date}"


class StockDetail(models.Model):
    transaction = models.ForeignKey(StockTransaction, on_delete=models.CASCADE, related_name='details')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def clean(self):
        if self.transaction.transaction_type == 'OUT':
            # calculate current stock
            from .utils import get_product_stock
            current_stock = get_product_stock(self.product.id)
            if self.quantity > current_stock:
                raise ValidationError(f"Insufficient stock for {self.product.name}")

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"


# Create your models here.
