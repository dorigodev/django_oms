from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib import auth
from apps.users.models import SupplierUser, BuyerUser, AdressUser
from apps.users.forms import LoginForm, SupplierForm, AdressUserForm, BuyerUserForm

User = get_user_model()

class UserViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

        # Create a test user for login tests
        self.user_password = 'testpassword'
        self.user = SupplierUser.objects.create_user(
            username='testuser', email='testuser@example.com', password=self.user_password
        )
        self.adress = AdressUser.objects.create(cep='12345', number='10', complement='Apt 101')
        self.buyer_user = BuyerUser.objects.create(user=self.user, cnpj='12345678901234', phone_number='1234567890', adress=self.adress)

        # URLs for each view
        self.login_url = reverse('users:login_user')
        self.register_url = reverse('users:create_user')
        self.logout_url = reverse('users:logout_user')
        self.change_password_url = reverse('users:change_password')

    def test_login_user_view_get(self):
        """Test GET request for login_user view renders the login form."""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')
        self.assertIsInstance(response.context['form'], LoginForm)

    def test_login_user_view_post_invalid(self):
        """Test POST request with invalid credentials does not log the user in."""
        response = self.client.post(self.login_url, {
            'store_email_login': 'wrong@example.com',
            'store_password_login': 'wrongpassword',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')
        self.assertFalse(auth.get_user(self.client).is_authenticated)

    def test_create_user_view_get(self):
        """Test GET request for create_user view renders the registration form."""
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register_teste.html')
        self.assertIsInstance(response.context['SupplierForm'], SupplierForm)
        self.assertIsInstance(response.context['AdressUserForm'], AdressUserForm)
        self.assertIsInstance(response.context['BuyerUserForm'], BuyerUserForm)


    def test_change_password_view_get(self):
        """Test GET request to change password page for logged-in user."""
        self.client.login(email=self.user.email, password=self.user_password)
        response = self.client.get(self.change_password_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/change_password.html')

    def test_change_password_view_post_invalid(self):
        """Test POST request with invalid data does not change the password."""
        self.client.login(email=self.user.email, password=self.user_password)
        response = self.client.post(self.change_password_url, {
            'old_password': self.user_password,
            'new_password1': 'newpassword123',
            'new_password2': 'differentpassword',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/change_password.html')
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(self.user_password))  # Password should remain the same