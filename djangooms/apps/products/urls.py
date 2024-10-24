from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf.urls.static import static
from django.conf import settings
from apps.products.views import index
from apps.products.views import create_product
from apps.products.views import update_product
from apps.products.views import delete_product
from apps.products.views import search_product

app_name = 'products'

urlpatterns = [
    path('', index, name='index'),
    path('create_product', create_product, name='create_product'),
    path('update_product/<int:product_id>', update_product, name='update_product'),
    path('delete_product/<int:product_id>', delete_product, name='delete_product'),
    path('search_product', search_product, name='search_product'),
]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )