import datetime
from django.shortcuts import render
from django.shortcuts import redirect
from apps.orders.forms import OrderForm, OrdemItemFormSet, OrderUpdateForm
from apps.orders.models import Order
from apps.orders.models import OrderItem
from django.views.generic import TemplateView
from django.db.models import Sum
from apps.products.models import Product
# Create your views here.
def index(request):
    order = Order.objects.all()
    order_item = OrderItem.objects.all()

    return render(request, 'orders/order_list.html', {'order': order,
                                                      'order_item': order_item,
         })


class OrderAddView(TemplateView):
    template_name = 'orders/order.html'

    def get(self, *args, **kwargs):
        order_form = OrderForm()
        orderItem_Form = OrdemItemFormSet(queryset=OrderItem.objects.none())
        return self.render_to_response({'orderForm': order_form, 'orderItemForm': orderItem_Form, })

    def post(self, *args, **kwargs):
        order_form = OrderForm(data=self.request.POST)
        order_item_form = OrdemItemFormSet(data=self.request.POST)
        if order_item_form.is_valid() and order_form.is_valid():
            order = order_form.save()
            for order_item_form in order_item_form:
                if order_item_form.is_valid():
                    order_item = order_item_form.save()
                    order.shoppinglist.add(order_item)
            return redirect('products:index')


def update_order(request, order_id):
    order = Order.objects.get(pk=order_id)
    upadate_form = OrderUpdateForm(instance=order)
    if request.method == 'POST':
        form = OrderUpdateForm(request.POST, instance=order)
        if form.is_valid():
            if form.cleaned_data['status'] == 'Finished':
                order.completionDate = datetime.datetime.now()
            form.save()

            return redirect('products:index')
    return render(request, 'orders/update_order.html', {'updateForm': upadate_form})


def dashboard(request):

    all_orders = Order.objects.all()

    total_orders = all_orders.count()

    total_order_profit = []
    if all_orders:
        for order in all_orders:
            total_order_profit.append(order.get_total_profit())
            total_order_profit_sum = round(sum(total_order_profit),2)


    total_order_price = []
    if all_orders:
        for order in all_orders:
            total_order_price.append(order.get_total_cost())
            total_order_price_sum = round(sum(total_order_price),2)

    total_value = sum(order.get_total_cost() for order in all_orders)
    medium_ticket = round(total_value / total_orders, 2) if total_orders else 0

    mais_vendidos = (
        OrderItem.objects.values('item')
        .annotate(total_vendido=Sum('quantity'))
        .order_by('-total_vendido')[:5]
    )

    product_ids = [p['item'] for p in mais_vendidos]
    products = Product.objects.filter(id__in=product_ids)
    product_map = {p.id: p for p in products}

    ranking = []
    for p in mais_vendidos:
        produto = product_map.get(p['item'])
        if produto:
            ranking.append({
                'nome': produto.name,
                'preco': produto.price,
                'custo': produto.cost,
                'lucro': produto.get_lucro(),
                'foto_url': produto.get_photo_url(),
                'quantidade_vendida': p['total_vendido'],
            })


    return render(request, 'orders/dashboard.html',
                  {'order': all_orders,
                      'pedidos': total_orders
                   , 'total_order_price_sum': total_order_price_sum,
                   'total_order_profit_sum': total_order_profit_sum,
                   'medium_ticket': medium_ticket,
                   "ranking": ranking,})