# Generated by Django 5.1.2 on 2024-10-14 15:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.FloatField(max_length=50)),
                ('weight', models.FloatField(max_length=50)),
                ('description', models.CharField(max_length=200)),
                ('quantity', models.IntegerField()),
                ('disponibility', models.BooleanField(default=True)),
                ('stockDate', models.DateField(verbose_name=models.DateTimeField(default=datetime.datetime.now))),
                ('productPhoto', models.ImageField(upload_to='products_photos/%Y/%m/%d/')),
            ],
        ),
    ]