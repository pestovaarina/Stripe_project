from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator


User = get_user_model()


class Item(models.Model):
    """Модель для класса товаров."""

    CURRENCY = [
        ('RUB', 'rub'),
        ('USD', 'usd'),
        ('EUR', 'eur')
    ]
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название товара'
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    price = models.IntegerField(
        validators=[
            MinValueValidator(0, 'Цена не может '
                              'быть менее нуля.'),
        ],
        verbose_name='Цена'
    )
    currency = models.CharField(
        max_length=5,
        choices=CURRENCY,
        default='RUB',
        verbose_name='Валюта оплаты'
    )

    def get_price_show(self):
        """Переводит цену из копеек в рубли."""
        return '{0:.2f}'.format(self.price / 100)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Order(models.Model):
    """Модель для класса заказ."""

    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='customer',
        verbose_name='Покупатель'
    )
    item = models.ManyToManyField(
        Item,
        through='ItemsOrder',
        related_name='item',
        verbose_name='Товары'
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ № {self.id}'


class Discount(models.Model):
    """Модель для класса скидка."""

    name = models.CharField(
        verbose_name='Название скидки',
        max_length=100
    )
    percentage = models.FloatField(
        verbose_name='Размер скидки',
        validators=[
            MinValueValidator(0.01),
            MaxValueValidator(100)
        ])
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='discount'
    )
    redeem_by = models.DateField(
        verbose_name='Срок действия',
        null=True,
        blank=True,
    )

    def __str__(self):
        return f'{self.name}, {self.percentage}'

    class Meta:
        verbose_name = 'Скидка'
        verbose_name_plural = 'Скидки'


class Tax(models.Model):
    """Модель для класса Налог."""

    display_name = models.CharField(
        max_length=100,
        verbose_name='Название')
    inclusive = models.BooleanField(
        default=False,
        verbose_name='Налог включен в стоимость'
    )
    percentage = models.FloatField(
        verbose_name='Размер налога',
        validators=[
            MinValueValidator(0.01),
            MaxValueValidator(100)
        ])

    def __str__(self):
        return f'{self.display_name}, {self.percentage}'

    class Meta:
        verbose_name = 'Налог'
        verbose_name_plural = 'Налоги'


class ItemsOrder(models.Model):
    """Промежуточная таблица для связи Товаров и Заказов."""

    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name='item_in_order',
        verbose_name='Товар'
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='order',
        verbose_name='Заказ'
    )
    amount = models.PositiveIntegerField(
        verbose_name='Количество',
        default=1,
        validators=[
            MinValueValidator(1, 'Количество не может быть меньше 1.'),
        ],
    )

    def __str__(self):
        return f'{self.item.name} в заказе {self.order.id}'
