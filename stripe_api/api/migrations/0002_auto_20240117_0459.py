# Generated by Django 3.2.3 on 2024-01-17 04:59

import django.core.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='discount',
            options={'verbose_name': 'Скидка', 'verbose_name_plural': 'Скидки'},
        ),
        migrations.AlterModelOptions(
            name='tax',
            options={'verbose_name': 'Налог', 'verbose_name_plural': 'Налоги'},
        ),
        migrations.AddField(
            model_name='tax',
            name='display_name',
            field=models.CharField(default=django.utils.timezone.now, max_length=100, verbose_name='Название'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tax',
            name='inclusive',
            field=models.BooleanField(default=False, verbose_name='Налог включен в стоимость'),
        ),
        migrations.AddField(
            model_name='tax',
            name='percentage',
            field=models.FloatField(default=15, validators=[django.core.validators.MinValueValidator(0.01), django.core.validators.MaxValueValidator(100)], verbose_name='Размер налога'),
            preserve_default=False,
        ),
    ]
