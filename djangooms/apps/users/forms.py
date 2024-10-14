from django import forms
from django.contrib import messages
import requests
import json
from django.contrib.auth.forms import UserCreationForm
# Pesquisar sobre: from django.contrib.auth import password_validation
from apps.users.models import StoreUser
from django.contrib.auth import get_user_model


class registerForm(UserCreationForm):
    store_name = forms.CharField(
        label='Nome da Loja',
        required=True,
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Digite o nome da sua loja'})
    )

    store_email = forms.EmailField(
        label='Email da loja',
        required=True,
        max_length=70,
        widget=forms.EmailInput(attrs={'class': 'form-control',
                                       'placeholder': 'Digite o e-mail da sua loja'})
    )

    store_CNPJ = forms.CharField(
        label='CNPJ da loja',
        required=True,
        max_length=14,
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Digite o CNPJ da sua loja, sem pontos ou traços'})
    )

    password1 = forms.CharField(
        label='Senha para acesso do painel da sua loja',
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                          'placeholder': 'Digite sua senha'})
    )

    password2 = forms.CharField(
        label='Digite novamente a senha para acesso do painel',
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                          'placeholder': 'Digite sua senha'})
    )

    class Meta:
        model = StoreUser
        fields = ['store_name', 'store_email', 'store_CNPJ', ]

    def clean_store_email(self):
        store_email = self.cleaned_data.get('store_email', '')
        exists = StoreUser.objects.filter(email=store_email).exists()
        if exists:
            raise forms.ValidationError('Email já cadastrado')
        return store_email

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError('Senhas diferentes uma da outra, verifique novamente')
            else:
                return password2

    def clean_store_CNPJ(self):
        cnaes_permitidos = ['8610101', '8630501', '8630502', '8650003', '8630505',
                            '8690903', '4729699', '4773300', '4775002', '4789099']
        store_CNPJ = self.cleaned_data['store_CNPJ']
        if StoreUser.objects.filter(cnpj=store_CNPJ).exists():
            raise forms.ValidationError('CNPJ já cadastrado')
        response = requests.get(f'https://brasilapi.com.br/api/cnpj/v1/{store_CNPJ}')
        if response.status_code == 200:
            data = response.json()
            if str(data['cnae_fiscal']) not in cnaes_permitidos:
                raise forms.ValidationError('O Cnae da sua empresa não é permitido para compras ')
        else:
            raise forms.ValidationError('Não foi possível validar o CNPJ. Verifique o número e tente novamente.')
        return store_CNPJ


class loginForm(forms.Form):
    store_email_login = forms.EmailField(
        label='Email da loja',
        required=True,
        max_length=70,
        widget=forms.EmailInput(attrs={'class': 'form-control',
                                       'placeholder': 'Digite o e-mail da sua loja'})
    )

    store_password_login = forms.CharField(
        label='Senha para acesso do painel da sua loja',
        required=True,
        max_length=70,
        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                          'placeholder': 'Digite sua senha'})
    )
