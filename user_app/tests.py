from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

# Create your tests here.

User = get_user_model()

class UserAPITests(APITestCase):

    def setUp(self):
        # Create a test user
        self.username = 'testuser'
        self.password = 'testpass'
        self.user = User.objects.create_user(username=self.username, password=self.password, email='test@example.com')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')

    def authenticate(self):
        response = self.client.post(self.login_url, data={'username': self.username, 'password': self.password})
        access_token = response.data['details']['access_token']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)

    def test_login_success(self):
        response = self.client.post(self.login_url, data={'username': self.username, 'password': self.password})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertIn('access_token', response.data['details'])

    def test_login_failure(self):
        response = self.client.post(self.login_url, data={'username': self.username, 'password': 'wrongpass'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['success'])

    def test_logout_success(self):
        self.authenticate()

        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
