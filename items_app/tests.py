
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from .models import Item
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your tests here.
class ItemAPITests(APITestCase):
    
    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpass'
        self.user = User.objects.create_user(username=self.username, password=self.password, email='test@example.com')
        self.item = Item.objects.create(name='Test Item', description='This is a test item', bln_active=True)
        print(f"Created item: {self.item.id} - {self.item.name}")
        self.login_url = reverse('login')
        self.item_url = reverse('item')
        self.item_detail_url = reverse('item-detail', args=[1])

    def authenticate(self):
        response = self.client.post(self.login_url, data={'username': self.username, 'password': self.password})
        access_token = response.data['details']['access_token']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)

    def test_get_item_detail(self):
        # import pdb;pdb.set_trace()
        self.authenticate()
        response = self.client.get(self.item_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['details']['name'], self.item.name)

    def test_get_item_list(self):
        self.authenticate()
        response = self.client.get(self.item_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['details']), 1)

    def test_create_item(self):
        self.authenticate()
        data = {
            'name': 'New Item',
            'description': 'This is a new item.'
        }
        response = self.client.post(self.item_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Item.objects.count(), 2)

    def test_update_item(self):
        self.authenticate()
        data = {
            'description': 'Updated description.'
        }
        response = self.client.put(self.item_detail_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.item.refresh_from_db()
        self.assertEqual(self.item.description, 'Updated description.')

    def test_delete_item(self):
        self.authenticate()
        response = self.client.delete(self.item_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.item.refresh_from_db()
        self.assertFalse(self.item.bln_active)

    def test_get_item_not_found(self):
        self.authenticate()
        response = self.client.get(reverse('item-detail', kwargs={'item_id': 99999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


