from django.contrib import admin
from apps.orders.models import Order


# Register your models here.
class ListingOrderAdmin(admin.ModelAdmin):
    list_display = ('id', "dateOrder", 'completionDate', 'shipping', 'status')
    list_display_links = ('id',)
    search_fields = ('id',)

admin.site.register(Order, ListingOrderAdmin)
