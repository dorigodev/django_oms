from django import forms
import requests
# Pesquisar sobre: from django.contrib.auth import password_validation
from apps.users.models import BuyerUser
from apps.users.models import SupplierUser
from apps.users.models import AdressUser


class SupplierForm(forms.ModelForm):
    class Meta:
        model = SupplierUser
        fields = 'store_name', 'store_email',

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

    def clean_store_email(self):
        store_email = self.cleaned_data.get('store_email', '')
        exists = SupplierUser.objects.filter(email=store_email).exists()
        if exists:
            raise forms.ValidationError('Email já cadastrado')
        return store_email


class AdressUserForm(forms.ModelForm):
    class Meta:
        model = AdressUser
        fields = ['store_CEP', 'store_number', 'store_complement']

    store_CEP = forms.CharField(
        label='CEP da loja',
        required=True,
        max_length=10,
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Digite o CEP da sua loja'})
    )

    store_number = forms.CharField(
        label='Número da loja',
        required=True,
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Número da loja'})
    )

    store_complement = forms.CharField(
        label='Complemento da loja',
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Digite o complemento da sua loja, caso tiver'})
    )


class BuyerUserForm(forms.ModelForm):
    class Meta:
        model = BuyerUser
        fields = ['store_CNPJ', 'store_phone',]

    store_CNPJ = forms.CharField(
        label='CNPJ da loja',
        required=True,
        max_length=14,
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Digite o CNPJ da sua loja, sem pontos ou traços'})
    )

    store_phone = forms.CharField(
        label='Telefone da loja',
        required=True,
        max_length=25,
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Digite o Telefone da sua loja'})
    )

    def clean_store_CNPJ(self):
        cnaes_permitidos = ['8610101', '8630501', '8630502', '8650003', '8650002', '8630505',
                            '8690903', '4729699', '4773300', '4775002', '4789099']
        store_CNPJ = self.cleaned_data['store_CNPJ']
        if BuyerUser.objects.filter(cnpj=store_CNPJ).exists():
            raise forms.ValidationError('CNPJ já cadastrado')
        response = requests.get(f'https://publica.cnpj.ws/cnpj/{store_CNPJ}')
        if response.status_code == 200:
            data = response.json()
            if str(data['estabelecimento']['atividade_principal']['id']) not in cnaes_permitidos:
                raise forms.ValidationError('O Cnae da sua empresa não é permitido para compras ')
        else:
            raise forms.ValidationError('Não foi possível validar o CNPJ. Verifique o número e tente novamente.')
        return store_CNPJ


class LoginForm(forms.Form):
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

class changePasswordForm(forms.Form):
    old_password = forms.CharField(
        label='Senha atual',
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                          'placeholder': 'Digite sua senha atual'})
    )

    password1 = forms.CharField(
        label='Nova Senha',
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                          'placeholder': 'Digite sua nova senha'})
    )

    password2 = forms.CharField(
        label='Digite novamente a senha para acesso do painel',
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                          'placeholder': 'Digite novamente sua nova senha'})
    )

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError('Senhas diferentes uma da outra, verifique novamente')
            else:
                return password2