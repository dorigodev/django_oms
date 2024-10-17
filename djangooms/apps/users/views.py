from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import redirect
from apps.users.forms import LoginForm
from apps.users.forms import SupplierForm
from apps.users.forms import AdressUserForm
from apps.users.forms import BuyerUserForm
from django.template import RequestContext
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.views.generic.edit import CreateView
from apps.users.models import BuyerUser
from apps.users.models import SupplierUser
from apps.users.models import AdressUser
from django.contrib.auth import get_user_model


# Create your views here.


def login_user(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            store_email_login = form.cleaned_data['store_email_login']
            store_password_login = form.cleaned_data['store_password_login']
            user = auth.authenticate(request, email=store_email_login, password=store_password_login)
            if user is not None:
                auth.login(request, user)
                messages.success(request, 'You are now logged in!')
                return redirect('index')
            else:
                messages.error(request, 'Invalid email or password.')
    return render(request, 'users/login.html', {'form': form})


def create_user(request):
    Supplier_Form = SupplierForm()
    AdressUser_Form = AdressUserForm()
    BuyerUser_Form = BuyerUserForm()
    if request.method == 'POST':
        Supplier_Form = SupplierForm(request.POST)
        AdressUser_Form = AdressUserForm(request.POST)
        BuyerUser_Form = BuyerUserForm(request.POST)
        if Supplier_Form.is_valid() and AdressUser_Form.is_valid() and BuyerUser_Form.is_valid():
            store_name = Supplier_Form.cleaned_data.get('store_name')
            store_email = Supplier_Form.cleaned_data.get('store_email')
            password = Supplier_Form.cleaned_data.get('password2')
            store_CEP = AdressUser_Form.cleaned_data.get('store_CEP')
            store_number = AdressUser_Form.cleaned_data.get('store_number')
            store_complement = AdressUser_Form.cleaned_data.get('store_complement')
            store_CNPJ = BuyerUser_Form.cleaned_data.get('store_CNPJ')
            store_phone = BuyerUser_Form.cleaned_data.get('store_phone')
            new_user = SupplierUser.objects.create_user(username=store_name, email=store_email, password=password)
            new_adress = AdressUser.objects.create(cep=store_CEP, number=store_number,
                                                   complement=store_complement)
            newBuyer = BuyerUser.objects.create(user=new_user, cnpj=store_CNPJ, phone_number=store_phone,
                                                adress=new_adress)
            new_user.save()
            new_adress.save()
            newBuyer.save()
            messages.success(request, 'Your account has been created.')
            return redirect('login_user')
    return render(request, 'users/register_teste.html', {'SupplierForm': Supplier_Form, 'AdressUserForm':AdressUser_Form,
                                                                            'BuyerUserForm': BuyerUser_Form})


@csrf_exempt
def logout_user(request):
    auth.logout(request)
    messages.success(request, 'Logout efetuado com sucesso!')
    return redirect("login_user")
