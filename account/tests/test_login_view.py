import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestLoginView:
    
    def test_login_success_200(self, api_client, user_with_password):
        url = reverse('login')
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = api_client.post(url, data)
        
        assert response.status_code == 200
        assert 'user' in response.data
        assert 'token' in response.data
        assert response.data['user']['username'] == 'testuser'

    def test_login_invalid_credentials_400(self, api_client, user_with_password):
        url = reverse('login')
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = api_client.post(url, data)
        
        assert response.status_code == 400
        assert 'non_field_errors' in response.data

    def test_login_missing_username_400(self, api_client):
        url = reverse('login')
        data = {'password': 'testpass123'}
        response = api_client.post(url, data)
        
        assert response.status_code == 400

    def test_login_missing_password_400(self, api_client):
        url = reverse('login')
        data = {'username': 'testuser'}
        response = api_client.post(url, data)
        
        assert response.status_code == 400

    def test_login_nonexistent_user_400(self, api_client):
        url = reverse('login')
        data = {
            'username': 'nonexistent',
            'password': 'testpass123'
        }
        response = api_client.post(url, data)
        
        assert response.status_code == 400

    def test_login_inactive_user_400(self, api_client):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        User.objects.create_user(
            username='inactive',
            password='testpass123',
            is_active=False
        )
        url = reverse('login')
        data = {
            'username': 'inactive',
            'password': 'testpass123'
        }
        response = api_client.post(url, data)
        
        assert response.status_code == 400
