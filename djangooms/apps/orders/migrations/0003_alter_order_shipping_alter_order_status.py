# Generated by Django 5.1.2 on 2024-10-18 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_alter_orderitem_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='shipping',
            field=models.CharField(choices=[('Envio por Correios', 'Envio por Correios'), ('Retirada', 'Retirada')]),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Preparing', 'Preparing'), ('Delivered', 'Delivered'), ('Canceled', 'Canceled'), ('Finished', 'Finished')]),
        ),
    ]