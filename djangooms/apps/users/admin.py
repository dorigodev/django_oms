from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apps.users.models import SupplierUser, AdressUser, BuyerUser


# Register your models here.

class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'email', 'username',)
    search_fields = ('email', 'id')


class BuyerUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'cnpj', 'phone_number', 'adress', 'active')
    search_fields = ('user', 'cnpj', 'phone_number', 'adress')


class AdressUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'cep', 'number',)
    search_fields = ('id', 'cep')


admin.site.register(SupplierUser, CustomUserAdmin)
admin.site.register(BuyerUser, BuyerUserAdmin)
admin.site.register(AdressUser, AdressUserAdmin)
