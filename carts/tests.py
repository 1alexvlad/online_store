from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from django.http import JsonResponse

from product.models import Product, Category
from .models import Cart


class CartViewsTest(TestCase):
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
        self.client.force_login(self.user)


    def test_cart_add_view(self):
        url = reverse('carts:cart_add', kwargs={'product_slug': self.product.slug})
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, JsonResponse)
        
        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['total_quantity'], 1)
        self.assertEqual(data['item_quantity'], 1)
        self.assertEqual(data['product_name'], 'Test Product')
        
        # Проверяем, что товар добавился в корзину
        cart_item = Cart.objects.first()
        self.assertEqual(cart_item.quantity, 1)
        self.assertEqual(cart_item.product, self.product)
        self.assertEqual(cart_item.user, self.user)

    def test_cart_add_existing_item(self):
        Cart.objects.create(user=self.user, product=self.product, quantity=1)
        
        url = reverse('carts:cart_add', kwargs={'product_slug': self.product.slug})
        response = self.client.post(url)
        
        data = response.json()
        self.assertEqual(data['item_quantity'], 2)
        self.assertEqual(data['total_quantity'], 2)

    def test_cart_change_view_increase(self):
        cart_item = Cart.objects.create(user=self.user, product=self.product, quantity=1)
        
        url = reverse('carts:cart_change', kwargs={'product_slug': self.product.slug})
        response = self.client.post(url, {'action': 'increase'})
        
        data = response.json()
        self.assertEqual(data['item_quantity'], 2)
        self.assertEqual(data['total_quantity'], 2)

    def test_cart_change_view_decrease(self):
        cart_item = Cart.objects.create(user=self.user, product=self.product, quantity=2)
        
        url = reverse('carts:cart_change', kwargs={'product_slug': self.product.slug})
        response = self.client.post(url, {'action': 'decrease'})
        
        data = response.json()
        self.assertEqual(data['item_quantity'], 1)
        self.assertEqual(data['total_quantity'], 1)

    def test_cart_change_view_remove_when_quantity_1(self):
        cart_item = Cart.objects.create(user=self.user, product=self.product, quantity=1)
        
        url = reverse('carts:cart_change', kwargs={'product_slug': self.product.slug})
        response = self.client.post(url, {'action': 'decrease'})
        
        data = response.json()
        self.assertEqual(data['item_quantity'], 0)
        self.assertEqual(data['total_quantity'], 0)
        self.assertEqual(Cart.objects.count(), 0)

    def test_cart_remove_view(self):
        cart_item = Cart.objects.create(user=self.user, product=self.product, quantity=2)
        
        url = reverse('carts:cart_remove', kwargs={'cart_id': cart_item.id})
        response = self.client.post(url)
        
        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['total_quantity'], 0)
        self.assertEqual(Cart.objects.count(), 0)

    def test_cart_remove_view_unauthorized(self):
        other_user = User.objects.create_user(username='other', password='pass123')
        cart_item = Cart.objects.create(user=other_user, product=self.product, quantity=1)
        
        url = reverse('carts:cart_remove', kwargs={'cart_id': cart_item.id})
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, 404)  # Не должен найти чужую корзину