from django.contrib import admin
from apps.products.models import Product
# Register your models here.

class ListingProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name', 'price')


admin.site.register(Product, ListingProductAdmin)