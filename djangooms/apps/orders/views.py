from pyexpat.errors import messages
import datetime
from django.shortcuts import render
from django.shortcuts import redirect
from apps.orders.forms import OrderForm, OrdemItemFormSet, OrderUpdateForm
from apps.orders.models import Order
from apps.orders.models import OrderItem
from django.views.generic import ListView, TemplateView


# Create your views here.
def index(request):
    order = Order.objects.all()
    orderItem = OrderItem.objects.all()
    return render(request, 'orders/order_list.html', {'order': order, 'orderItem': orderItem})


class OrderAddView(TemplateView):
    template_name = 'orders/order.html'

    def get(self, *args, **kwargs):
        order_Form = OrderForm()
        orderItem_Form = OrdemItemFormSet(queryset=OrderItem.objects.none())
        return self.render_to_response({'orderForm': order_Form, 'orderItemForm': orderItem_Form, })

    def post(self, *args, **kwargs):
        order_Form = OrderForm(data=self.request.POST)
        orderItem_Form = OrdemItemFormSet(data=self.request.POST)
        if orderItem_Form.is_valid() and order_Form.is_valid():
            order = order_Form.save()
            for order_item_form in orderItem_Form:
                if order_item_form.is_valid():
                    order_item = order_item_form.save()
                    order.shoppinglist.add(order_item)
            return redirect('products:index')


def update_order(request, order_id):
    order = Order.objects.get(pk=order_id)
    upadateForm = OrderUpdateForm(instance=order)
    if request.method == 'POST':
        form = OrderUpdateForm(request.POST, instance=order)
        if form.is_valid():
            if form.cleaned_data['status'] == 'Finished':
                order.completionDate = datetime.datetime.now()
            form.save()

            return redirect('products:index')
    return render(request, 'orders/view_order.html', {'updateForm': upadateForm})
