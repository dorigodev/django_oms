from django.db import models
from django.contrib.auth import get_user_model
from djangooms.apps.products.models import Product


# Create your models here.
class OrderItem(models.Model):
    item = models.ForeignKey(to=Product, on_delete=models.CASCADE, null=False, blank=False)
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
    # ID (Já é colocado automaticamente)
    # Lista do que comprou (FK)
    shoppinglist = models.ManyToManyField(OrderItem, max_length=200)
    # loja que comprou
    store = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=False, blank=False)
    # status
    status = models.IntergerFiled(choices=STATUS_CHOICES, null=False, blank=False)
