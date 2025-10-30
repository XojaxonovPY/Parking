import pytest
from rest_framework.test import APIClient

from auth_user.models import User


class TestAuth:
    @pytest.fixture
    def client(self):
        user_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@gmail.com',
            'password': '1',
            'username': 'johndoe',
            'phone_number': '1234567890'
        }
        user = User.objects.create_user(**user_data)
        return APIClient()

    @pytest.mark.django_db
    def test_register(self, client):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'asqarservis00001@gmail.com',
            'password': '1',
            'username': 'botir'
        }
        response = client.post('http://localhost:8000/api/v1/register/')
        assert 200 >= response.status_code < 400
