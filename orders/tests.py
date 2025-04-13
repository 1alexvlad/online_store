from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages

from product.models import Product, Category
from carts.models import Cart

class CreateOrderViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )
        self.product = Product.objects.create(
            name='Test Product',
            price=100.00,
            slug='test-product',
            category=self.category
        )
        self.url = reverse('orders:create_order')

    def test_empty_cart_redirect(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url, {
            'phone_number': '1234567890',
            'requires_delivery': '0',
            'payment_on_get': '1'
        })
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Ваша корзина пуста!')
        self.assertEqual(response.status_code, 302)

    def test_successful_order_creation(self):
        self.client.force_login(self.user)
        Cart.objects.create(user=self.user, product=self.product, quantity=1)
        
        response = self.client.post(self.url, {
            'phone_number': '1234567890',
            'requires_delivery': '1',
            'delivery_address': 'Test address',
            'payment_on_get': '1'
        }, follow=True)
        
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Заказ успешно оформлен!')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Cart.objects.count(), 0)

    def test_order_with_card_payment(self):
        self.client.force_login(self.user)
        Cart.objects.create(user=self.user, product=self.product, quantity=1)
        
        response = self.client.post(self.url, {
            'phone_number': '1234567890',
            'requires_delivery': '0',
            'payment_on_get': '0',
            'card_number': '1111111111111111',
            'card_expiry': '12/25',
            'card_cvv': '123'
        })
        
        self.assertEqual(response.status_code, 302)