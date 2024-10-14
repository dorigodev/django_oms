from datetime import datetime
from django.db import models
# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    price = models.FloatField(max_length=50, null=False, blank=False)
    weight = models.FloatField(max_length=50, null=False, blank=False)
    description = models.CharField(max_length=200, null=False, blank=False)
    quantity = models.IntegerField(null=False, blank=False)
    disponibility = models.BooleanField(blank=False, default=True)
    stockDate = models.DateField(models.DateTimeField(default=datetime.now, null=False, blank=False))
    productPhoto = models.ImageField(upload_to='products_photos/%Y/%m/%d/', null=False, blank=False)

    def __str__(self):
        return self.name

    def get_disponibility(self):
        return self.disponibility

    def get_price(self):
        return self.price

    def get_quantity(self):
        return self.quantity

    def get_photo_url(self):
        if self.productPhoto:
            return getattr(self.productPhoto, 'url', None)
        return None

    def get_date_formated(self):
        return self.stockDate.strftime('%d/%m/%Y')

