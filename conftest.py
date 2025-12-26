import pytest
from model_bakery import baker
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from knox.models import AuthToken

User = get_user_model()


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        from account.models import RoleModel
        RoleModel.objects.get_or_create(role_name='admin')
        RoleModel.objects.get_or_create(role_name='editor')
        RoleModel.objects.get_or_create(role_name='viewer')


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def admin_role():
    from account.models import RoleModel
    return RoleModel.objects.get_or_create(role_name='admin')[0]


@pytest.fixture
def editor_role():
    from account.models import RoleModel
    return RoleModel.objects.get_or_create(role_name='editor')[0]


@pytest.fixture
def viewer_role():
    from account.models import RoleModel
    return RoleModel.objects.get_or_create(role_name='viewer')[0]


@pytest.fixture
def admin_user(admin_role):
    return User.objects.create_user(
        username='admin',
        email='admin@example.com',
        password='admin123',
        role=admin_role
    )


@pytest.fixture
def editor_user(editor_role):
    return User.objects.create_user(
        username='editor',
        email='editor@example.com',
        password='editor123',
        role=editor_role
    )


@pytest.fixture
def viewer_user(viewer_role):
    return User.objects.create_user(
        username='viewer',
        email='viewer@example.com',
        password='viewer123',
        role=viewer_role
    )


@pytest.fixture
def superuser():
    return User.objects.create_superuser(
        username='superuser',
        email='super@example.com',
        password='super123'
    )


@pytest.fixture
def admin_client(api_client, admin_user):
    _, token = AuthToken.objects.create(admin_user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    api_client.user = admin_user
    return api_client


@pytest.fixture
def editor_client(api_client, editor_user):
    _, token = AuthToken.objects.create(editor_user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    api_client.user = editor_user
    return api_client


@pytest.fixture
def viewer_client(api_client, viewer_user):
    _, token = AuthToken.objects.create(viewer_user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    api_client.user = viewer_user
    return api_client


@pytest.fixture
def superuser_client(api_client, superuser):
    _, token = AuthToken.objects.create(superuser)
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    api_client.user = superuser
    return api_client


@pytest.fixture
def user(viewer_role):
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123',
        role=viewer_role
    )


@pytest.fixture
def user_with_password(viewer_role):
    user = User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123',
        role=viewer_role
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
def document(viewer_user):
    from document.models import DocumentModel
    return baker.make(
        DocumentModel,
        title='Test Document',
        description='Test Description',
        file_name='test.pdf',
        file_path='documents/test.pdf',
        file_size=1024,
        content_type='application/pdf',
        uploaded_by=viewer_user
    )
