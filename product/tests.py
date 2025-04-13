from django.test import TestCase, RequestFactory
from django.urls import reverse
from product.models import Category, Product

class CatalogProductViewTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Test Category",
            slug="test-category"
        )
        self.product = Product.objects.create(
            name="Test Product",
            price=100.00,
            slug="test-product",
            category=self.category
        )
        self.factory = RequestFactory()

    def test_catalog_view_status_code(self):
        response = self.client.get(reverse('product:catalog'))
        self.assertEqual(response.status_code, 200)

    def test_catalog_view_template(self):
        response = self.client.get(reverse('product:catalog'))
        self.assertTemplateUsed(response, 'product/catalog.html')

    def test_catalog_view_context(self):
        response = self.client.get(reverse('product:catalog'))
        self.assertIn('products', response.context)
        self.assertIn('categories', response.context)

    def test_catalog_filter_by_category(self):
        response = self.client.get(
            reverse('product:catalog') + '?category=test-category'
        )
        self.assertEqual(len(response.context['products']), 1)
        self.assertEqual(response.context['current_category'], 'test-category')


class ProductDetailViewTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Test Category",
            slug="test-category"
        )
        self.product = Product.objects.create(
            name="Test Product",
            price=100.00,
            slug="test-product",
            category=self.category
        )

    def test_product_detail_view_status_code(self):
        url = reverse('product:product_detail', kwargs={'slug': 'test-product'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_product_detail_view_template(self):
        url = reverse('product:product_detail', kwargs={'slug': 'test-product'})
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'product/product_detail.html')

    def test_product_detail_view_context(self):
        url = reverse('product:product_detail', kwargs={'slug': self.product.slug})  
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
