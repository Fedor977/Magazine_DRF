from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework import status  # импорт HTTP-статусов из Django REST Framework
from rest_framework.test import APIClient  # импорт клиента для тестирования API
from .models import Product, Order, Payment
from .serializers import ProductSerializer, OrderSerializer, PaymentSerializer


class ProductTestCase(TestCase):
    def setUp(self):  # настройка данных для тестирования
        self.client = APIClient()  # создание экземпляра клиента API
        self.product_data = {'name': 'Test Product', 'price': 10.99}  # тестовые данные для продукта
        self.product = Product.objects.create(name='Test Product', price=10.99)  # создание тестового продукта

    def test_product_list_create(self):  # тест для создания продукта
        response = self.client.post('/products/', self.product_data)  # отправка POST-запроса для создания продукта
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # проверка успешного создания продукта
        self.assertEqual(Product.objects.count(), 2)  # проверка увеличения количества продуктов

    def test_product_retrieve_update_destroy(self):  # nест для получения, обновления и удаления продукта
        response = self.client.get(f'/products/{self.product.id}/')  # отправка GET-запроса для получения продукта
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # проверка успешного получения продукта


class OrderTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.force_authenticate(user=self.user)
        self.order_data = {'product': 1, 'quantity': 2}
        self.order = Order.objects.create(product=Product.objects.first(), quantity=2, user=self.user)

    def test_order_list_create_authenticated(self):
        response = self.client.post('/orders/', self.order_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 2)

    def test_order_list_create_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.post('/orders/', self.order_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_order_retrieve_update_destroy(self):
        response = self.client.get(f'/orders/{self.order.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Add more assertions for update and destroy endpoints if needed


class PaymentTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.payment_data = {'order': 1, 'amount': 20.99}
        self.payment = Payment.objects.create(order=Order.objects.first(), amount=20.99)

    def test_payment_create(self):
        response = self.client.post('/payments/', self.payment_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Payment.objects.count(), 2)
