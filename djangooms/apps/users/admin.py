from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apps.users.models import StoreUser
# Register your models here.

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'cnpj')
    search_fields = ('cnpj', 'email')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email', 'cnpj')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

admin.site.register(StoreUser, CustomUserAdmin)