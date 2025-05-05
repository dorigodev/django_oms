from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf.urls.static import static
from django.conf import settings
from apps.orders.views import OrderAddView, index
from apps.orders.views import update_order
from apps.orders.views import dashboard

app_name = 'orders'
urlpatterns = [
    path('create_order', OrderAddView.as_view(), name='create_order'),
    path('view_order', index, name='view_order'),
    path('dashboard', dashboard, name='dashboard'),
    path('update_order/<int:order_id>', update_order, name='update_order'),
]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
