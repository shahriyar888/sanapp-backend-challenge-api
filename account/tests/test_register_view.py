import pytest
from django.urls import reverse
from django.contrib.auth.models import User


@pytest.mark.django_db
class TestRegisterView:
    
    def test_register_success_201(self, api_client):
        url = reverse('register')
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'securepass123',
            'password_confirm': 'securepass123'
        }
        response = api_client.post(url, data)
        
        assert response.status_code == 201
        assert 'user' in response.data
        assert 'token' in response.data
        assert response.data['user']['username'] == 'newuser'
        assert User.objects.filter(username='newuser').exists()

    def test_register_password_mismatch_400(self, api_client):
        url = reverse('register')
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'securepass123',
            'password_confirm': 'differentpass'
        }
        response = api_client.post(url, data)
        
        assert response.status_code == 400
        assert 'non_field_errors' in response.data or 'password' in str(response.data)

    def test_register_missing_fields_400(self, api_client):
        url = reverse('register')
        data = {'username': 'newuser'}
        response = api_client.post(url, data)
        
        assert response.status_code == 400

    def test_register_duplicate_username_400(self, api_client, user):
        url = reverse('register')
        data = {
            'username': user.username,
            'email': 'another@example.com',
            'password': 'securepass123',
            'password_confirm': 'securepass123'
        }
        response = api_client.post(url, data)
        
        assert response.status_code == 400

    def test_register_short_password_400(self, api_client):
        url = reverse('register')
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'short',
            'password_confirm': 'short'
        }
        response = api_client.post(url, data)
        
        assert response.status_code == 400
