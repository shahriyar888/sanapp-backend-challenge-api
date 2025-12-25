import pytest
from model_bakery import baker
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from knox.models import AuthToken


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return baker.make(User, username='testuser', email='test@example.com', is_active=True)


@pytest.fixture
def user_with_password():
    user = User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )
    return user


@pytest.fixture
def auth_token(user):
    _, token = AuthToken.objects.create(user)
    return token


@pytest.fixture
def authenticated_client(api_client, user, auth_token):
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {auth_token}')
    api_client.user = user
    return api_client


@pytest.fixture
def document(user):
    from document.models import DocumentModel
    return baker.make(
        DocumentModel,
        title='Test Document',
        description='Test Description',
        file_name='test.pdf',
        file_path='documents/test.pdf',
        file_size=1024,
        content_type='application/pdf',
        uploaded_by=user
    )
