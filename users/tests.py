from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User

class UserRegistrationTest(APITestCase):
    def test_register_supplier(self):
        url = reverse('user-register')
        data = {
            'email': 'supplier@example.com',
            'password': 'testpassword',
            'user_type': 'supplier'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'supplier@example.com')

    def test_register_consumer(self):
        url = reverse('user-register')
        data = {
            'email': 'consumer@example.com',
            'password': 'testpassword',
            'user_type': 'consumer'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'consumer@example.com')

    def test_register_invalid_user_type(self):
        url = reverse('user-register')
        data = {
            'email': 'invalid@example.com',
            'password': 'testpassword',
            'user_type': 'invalid_type'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class UserAuthenticationTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='user@example.com', password='testpassword')

    def test_authenticate_user(self):
        url = reverse('user-login')
        data = {
            'email': 'user@example.com',
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticate_invalid_user(self):
        url = reverse('user-login')
        data = {
            'email': 'user@example.com',
            'password': 'wrongpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)