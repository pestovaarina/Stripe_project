# Generated by Django 3.2.3 on 2024-01-11 13:44

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='Название товара')),
                ('description', models.TextField(verbose_name='Описание')),
                ('price', models.IntegerField(validators=[django.core.validators.MinValueValidator(0, 'Цена не может быть менее нуля.')], verbose_name='Цена')),
                ('currency', models.CharField(choices=[('RUB', 'rub'), ('USD', 'usd'), ('EUR', 'eur')], default='RUB', max_length=5, verbose_name='Валюта оплаты')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
            },
        ),
        migrations.CreateModel(
            name='ItemsOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1, 'Количество не может быть меньше 1.')], verbose_name='Количество')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='item_in_order', to='api.item', verbose_name='Товар')),
            ],
        ),
        migrations.CreateModel(
            name='Tax',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer', to=settings.AUTH_USER_MODEL, verbose_name='Покупатель')),
                ('item', models.ManyToManyField(related_name='item', through='api.ItemsOrder', to='api.Item', verbose_name='Товары')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
        migrations.AddField(
            model_name='itemsorder',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order', to='api.order', verbose_name='Заказ'),
        ),
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название скидки')),
                ('percentage', models.FloatField(validators=[django.core.validators.MinValueValidator(0.01), django.core.validators.MaxValueValidator(100)], verbose_name='Размер скидки')),
                ('redeem_by', models.DateField(blank=True, null=True, verbose_name='Срок действия')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='discount', to='api.order')),
            ],
        ),
    ]
