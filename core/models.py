from django.db import models
from django.contrib.auth.models import User
from autoslug import AutoSlugField
from django.utils.text import slugify


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование продукта')
    description = models.TextField(max_length=1000, verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    quantity_available = models.PositiveIntegerField(verbose_name='Количество')
    slug = AutoSlugField(unique=True, populate_from='name')  # AutoSlugField для автоматической генерации slug

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    products = models.ManyToManyField('Product', through='OrderItem', verbose_name='Продукт')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Время обновления')
    status = models.CharField(max_length=50, verbose_name='Статус')

    def __str__(self):
        return self.products

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма')

    def __str__(self):
        return self.order

    class Meta:
        verbose_name = 'Детали заказа'
        verbose_name_plural = 'Детали заказа'


class Payment(models.Model):
    order = models.OneToOneField('Order', on_delete=models.CASCADE, verbose_name='Заказ')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Количество')
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата оплаты')

    def __str__(self):
        return self.order

    class Meta:
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'



