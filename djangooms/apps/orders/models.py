from django.db import models
from django.contrib.auth import get_user_model
from apps.products.models import Product
from apps.users.models import BuyerUser
from datetime import datetime


# Create your models here.
class OrderItem(models.Model):
    item = models.ForeignKey(Product, on_delete=models.CASCADE, null=False, blank=False)
    quantity = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return f'{self.quantity} of {self.item}'

    def get_total_item_price(self):
        return self.item.price * self.quantity


class Order(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Preparing', 'Preparing'),
        ('Delivered', 'Delivered'),
        ('Canceled', 'Canceled'),
        ('Finished', 'Finished'),
    )

    SHIPPING_METHOD = (
        ('Envio por Correios', 'Envio por Correios'),
        ('Retirada', 'Retirada'),
    )

    # ID (Já é colocado automaticamente)
    id = models.AutoField(primary_key=True)
    # loja que comprou
    store = models.ForeignKey(BuyerUser, on_delete=models.CASCADE, null=False, blank=False, related_name='buyer_user')
    # Lista do que comprou (FK)
    shoppinglist = models.ManyToManyField(OrderItem, max_length=200, related_name='orderlist')
    # Data que foi realizada o pedido
    dateOrder = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    # Data que foi concluida
    completionDate = models.DateTimeField(null=True, blank=True)
    # Forma de envio
    shipping = models.CharField(choices=SHIPPING_METHOD, null=False, blank=False)
    # status
    status = models.CharField(choices=STATUS_CHOICES, null=False, blank=False, default='Pending')
