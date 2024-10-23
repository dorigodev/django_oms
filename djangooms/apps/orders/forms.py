from django import forms
from apps.orders.models import Order
from apps.orders.models import OrderItem
from django.forms import modelformset_factory


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('store', 'shipping',)


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ('item', 'quantity')


OrdemItemFormSet = modelformset_factory(
    OrderItem,
    form=OrderItemForm,
    fields=('item', 'quantity'),
    extra=1
)


class OrderUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('status',)
