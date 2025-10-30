from django.contrib.auth.hashers import make_password
from django.test import TestCase
from rest_framework.test import APIClient
from auth_user.models import User


class AuthTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            first_name='John',
            last_name='Doe',
            email='john@gmail.com',
            password='1',
            username='johndoe',
            role='admin'
        )

    def login(self):
        data = {
            'email': 'john@gmail.com',
            'password': '1'
        }
        response = self.client.post('/api/v1/login/', data)
        return response.data.get('access')

    def test_register_user(self):
        """Foydalanuvchini ro‘yxatdan o‘tkazish testi"""
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'asqarservis00001@gmail.com',
            'password': '12345',
            'username': 'botir',
        }
        response = self.client.post('/api/v1/register/', data)
        self.assertTrue(200 <= response.status_code < 300, 'User not created')

    def test_login(self):
        data = {
            'email': 'john@gmail.com',
            'password': '1'
        }
        response = self.client.post('/api/v1/login/', data)
        self.assertTrue(200 <= response.status_code < 300, 'User not found')
        self.assertTrue(response.data.get('access'), 'token not found')

    def test_forgot_password(self):
        data = {
            "email": "john@gmail.com",
            "password": "1",
            "confirm_password": "1"
        }
        response = self.client.patch('/api/v1/forgot/password/', data, format='json')
        self.assertTrue(200 <= response.status_code < 300, 'Password not changed')
        self.assertTrue(response.json().get('new_password'), 'Password not changed')

    def test_user_get(self):
        response = self.client.get(
            '/api/v1/get/user',
            headers={"Authorization": f"Bearer {self.login()}"}
        )
        self.assertTrue(200 <= response.status_code < 300, 'User not found')
        self.assertEqual(
            response.json().get('first_name'),
            'John',
            'User not found'
        )

    def test_get_all_users(self):
        response = self.client.get('/api/v1/get/all/users', headers={"Authorization": f"Bearer {self.login()}"})
        self.assertTrue(200 <= response.status_code < 300, 'Users not found')

    def test_delete_user(self):
        response = self.client.delete(
            '/api/v1/delete/users/2',
            headers={"Authorization": f"Bearer {self.login()}"}
        )
        self.assertTrue(200 <= response.status_code < 300, 'User not deleted')

    def test_update_user(self):
        data = {
            'first_name': 'botir',
            'last_name': 'ali',
            'email': 'doe@gmail.com',
            'username': 'ali',
        }
        response = self.client.put(
            '/api/v1/update/user',
            headers={"Authorization": f"Bearer {self.login()}"},
            data=data,
            format='json'
        )
        self.assertTrue(200 <= response.status_code < 300, 'User not updated')
        self.assertEqual(response.json()[0].get('first_name'), 'botir', 'value not changed')
