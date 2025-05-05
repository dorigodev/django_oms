from django import forms
from apps.products.models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['disponibility',]
        labels = {
            'name': 'Nome do Produto',
            'price': 'Preço do Produto',
            'cost':"Custo de produção",
            'weight': 'Peso do produto em kilos, considere: 0.150 para 60 caps, e 0.200 para 120 caps',
            'description': 'Breve descrição sobre o produto',
            'quantity': 'Quantidade do produto em stock',
            'disponibility': 'Disponibilidade do Produto',
            'stockDate':'Data de compra do produto',
            'productPhoto':'Foto do produto, caso tenha',
        }

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'cost': forms.NumberInput(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'stockDate': forms.DateTimeInput(format='%d/%m/%Y',
                                         attrs={'class': 'form-control', 'type': 'date',}),
            'productPhoto': forms.FileInput(attrs={'class': 'form-control'}),
    }

