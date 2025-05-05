
# Create your views here.
from django.shortcuts import render
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import redirect
from apps.products.models import Product
from apps.products.forms import ProductForm


# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        messages.error(request, 'You are not logged in!')
        return redirect('users:login_user')
    products = Product.objects.filter(disponibility=True)
    # faz a contagem dos produtos
    products_count = products.count()

    # faz a contagem de quanto em dinheiro tem no estoque
    total_stock_price = []
    if products:
        for product in products:
            quantity = product.get_quantity()
            price = product.get_price()
            total_price = quantity * price
            total_stock_price.append(total_price)
            new_total_stock_price = sum(total_stock_price)
    else:
        new_total_stock_price = 0

    # faz a contagem de quantos produtos tem em estoque
    products_quantity = []
    if products:
        for product in products:
            quantity = product.get_quantity()
            products_quantity.append(quantity)
        quantity_total = sum(products_quantity)
    else:
        quantity_total = 0

    return render(request, 'stock/index.html', {'products': products,
                                                'products_variety':products_count,
                                                'total_price':new_total_stock_price,
                                                'quantity': quantity_total,
                                                })


def create_product(request):
    products = Product.objects.filter(disponibility=True)
    Form = ProductForm()
    if not request.user.is_authenticated:
        messages.error(request, 'You are not logged in!')
        return redirect('users:login_user')
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.save()
            messages.success(request, 'Product successfully created')
            return redirect('products:index')
    return render(request, 'stock/create_product.html', {'form':Form, 'products':products})
def update_product(request, product_id):
    product_object = Product.objects.get(id=product_id)
    form = ProductForm(instance=product_object)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product_object)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product successfully updated')
            return redirect('products:index')
    return render(request, 'stock/update_product.html', {'form':form, 'product':product_object, 'product_id':product_id})

def delete_product(request, product_id):
    product_object = Product.objects.get(id=product_id)
    product_object.disponibility = False
    product_object.save()
    messages.success(request, 'Producto deletado com sucesso')
    return redirect("products:index")

def search_product(request):
    if not request.user.is_authenticated:
        messages.error(request, 'You are not logged in!')
        return redirect('users:login_user')
    products = Product.objects.filter(disponibility=True)
    if 'search' in request.GET:
        search = request.GET['search']
        if search:
            products = products.filter(Q(name__icontains=search) | Q(id__icontains=search))

        # faz a contagem dos produtos
        products_count = products.count()

        # faz a contagem de quanto em dinheiro tem no estoque
        total_stock_price = []
        if products:
            for product in products:
                quantity = product.get_quantity()
                price = product.get_price()
                total_price = quantity * price
                total_stock_price.append(total_price)
                new_total_stock_price = sum(total_stock_price)
        else:
            new_total_stock_price = 0

        # faz a contagem de quantos produtos tem em estoque
        products_quantity = []
        if products:
            for product in products:
                quantity = product.get_quantity()
                products_quantity.append(quantity)
            quantity_total = sum(products_quantity)
        else:
            quantity_total = 0

    return render(request, 'stock/index.html', {'products': products, 'products_variety':products_count, 'total_price':new_total_stock_price, 'quantity': quantity_total})


