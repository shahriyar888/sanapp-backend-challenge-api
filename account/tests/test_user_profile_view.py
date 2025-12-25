import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestUserProfileView:
    
    def test_get_profile_success_200(self, authenticated_client):
        url = reverse('user-profile')
        response = authenticated_client.get(url)
        
        assert response.status_code == 200
        assert 'username' in response.data
        assert response.data['username'] == authenticated_client.user.username

    def test_get_profile_unauthorized_401(self, api_client):
        url = reverse('user-profile')
        response = api_client.get(url)
        
        assert response.status_code == 401
