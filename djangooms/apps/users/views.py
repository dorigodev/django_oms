from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import redirect
from apps.users.forms import registerForm, loginForm
from django.template import RequestContext
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.views.generic.edit import CreateView
from apps.users.models import StoreUser
from django.contrib.auth import get_user_model

# Create your views here.


def login_user(request):
    form = loginForm()
    if request.method == 'POST':
        form = loginForm(request.POST)
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
    user = get_user_model()
    if request.method == 'POST':
        form = registerForm(request.POST)
        if form.is_valid():
            store_name = form.cleaned_data.get('store_name')
            store_email = form.cleaned_data.get('store_email')
            store_CNPJ = form.cleaned_data.get('store_CNPJ')
            password = form.cleaned_data.get('password2')
            new_store = user.objects.create_user(username=store_name, email=store_email, password=password,
                                                 cnpj=store_CNPJ)
            new_store.save()
            messages.success(request, 'Your account has been created.')
            return redirect('login_user')
    else:
        form = registerForm()
    return render(request, 'users/register.html', {'form': form}, )

@csrf_exempt
def logout_user(request):
    auth.logout(request)
    messages.success(request, 'Logout efetuado com sucesso!')
    return redirect("login_user")
