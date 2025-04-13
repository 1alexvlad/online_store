from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.models import User

class RegistrationViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.url = reverse('account:register')

    def test_registration_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/register.html')

    def test_registration_post(self):
        data = {
            'username': 'newuser',
            'password1': 'complexpass123',
            'password2': 'complexpass123'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('product:index'))
        self.assertTrue(User.objects.filter(username='newuser').exists())

class UserLoginViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        cls.url = reverse('account:login')

    def test_login_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_login_post(self):
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('product:index'))

    def test_login_with_next(self):
        next_url = reverse('account:profile')
        data = {
            'username': 'testuser',
            'password': 'testpass123',
            'next': next_url
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, next_url)

class LogoutViewTest(TestCase):
    def test_logout(self):
        user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('account:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('product:index'))

class ProfileViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.url = reverse('account:profile')

    def test_profile_unauthorized(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('account:login'), response.url)

    def test_profile_authorized(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/profile.html')

class UsersCartViewTest(TestCase):
    def test_users_cart(self):
        response = self.client.get(reverse('account:users-cart'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/users_cart.html')


class UserFlowTest(TestCase):
    def test_user_registration_login_logout_flow(self):
        # Регистрация
        register_data = {
            'username': 'newuser',
            'password1': 'complexpass123',
            'password2': 'complexpass123'
        }
        response = self.client.post(reverse('account:register'), register_data)
        self.assertEqual(response.status_code, 302)
        
        # Логин
        login_data = {
            'username': 'newuser',
            'password': 'complexpass123'
        }
        response = self.client.post(reverse('account:login'), login_data)
        self.assertEqual(response.status_code, 302)
        
        # Проверка профиля
        response = self.client.get(reverse('account:profile'))
        self.assertEqual(response.status_code, 200)
        
        # Логаут
        response = self.client.get(reverse('account:logout'))
        self.assertEqual(response.status_code, 302)
        
        # Проверка доступа к профилю после выхода
        response = self.client.get(reverse('account:profile'))
        self.assertEqual(response.status_code, 302)
