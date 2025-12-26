# Test Suite Documentation

Comprehensive testing guide for the Django REST API project.

## 🛠️ Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Test Environment

Tests use SQLite by default (configured in `conftest.py`). No additional setup needed.

## 📝 Running Tests

### Run All Tests

```bash
pytest
```

### Run Specific Test Files

```bash
# Account tests
pytest account/tests/test_register_view.py
pytest account/tests/test_login_view.py
pytest account/tests/test_user_profile_view.py

# Document tests
pytest document/tests/test_document_viewset.py
pytest document/tests/test_document_rbac.py
```

### Run Specific Test Functions

```bash
pytest account/tests/test_register_view.py::TestRegisterView::test_register_success
pytest document/tests/test_document_viewset.py::TestDocumentViewSet::test_create_document
```

### Run with Verbose Output

```bash
pytest -v
```

### Run with Coverage Report

```bash
# Generate coverage report
pytest --cov=. --cov-report=html

# View coverage report
# Windows
start htmlcov/index.html

# Linux/macOS
open htmlcov/index.html
```

### Run Tests in Parallel (Faster)

```bash
pytest -n auto
```

## 📚 Test Structure

```
├── conftest.py                    # Shared fixtures
├── pytest.ini                     # Pytest configuration
├── account/tests/
│   ├── test_register_view.py      # User registration tests
│   ├── test_login_view.py         # User login tests
│   └── test_user_profile_view.py  # User profile tests
└── document/tests/
    ├── test_document_viewset.py   # Document CRUD tests
    └── test_document_rbac.py      # Document RBAC tests
```

## 🧰 Available Fixtures

Defined in `conftest.py`:

### Basic Fixtures
- `api_client` - Unauthenticated DRF API client
- `user` - Basic user instance (no password)
- `user_with_password` - User with password set to "testpass123"

### Authentication Fixtures
- `auth_token` - Knox authentication token for user
- `authenticated_client` - API client with authentication headers

### Document Fixtures
- `document` - Document instance owned by user

### Usage Example

```python
def test_example(authenticated_client, document):
    response = authenticated_client.get(f'/api/documents/{document.id}/')
    assert response.status_code == 200
```

## 📋 Test Coverage

### Account App Tests

**test_register_view.py**
- ✅ Successful registration (201)
- ✅ Invalid data validation (400)
- ✅ Duplicate username/email (400)

**test_login_view.py**
- ✅ Successful login (200)
- ✅ Invalid credentials (400)
- ✅ Token generation

**test_user_profile_view.py**
- ✅ Get authenticated user profile (200)
- ✅ Unauthorized access (401)
- ✅ Update user profile

### Document App Tests

**test_document_viewset.py**
- ✅ List documents (200)
- ✅ Create document (201)
- ✅ Retrieve document (200)
- ✅ Update document (200)
- ✅ Delete document (204)
- ✅ Unauthorized access (401)
- ✅ Not found (404)
- ✅ Invalid data (400)

**test_document_rbac.py**
- ✅ Owner permissions
- ✅ Editor permissions
- ✅ Viewer permissions
- ✅ Permission denied scenarios

## 🔧 Pytest Configuration

`pytest.ini` settings:

```ini
[pytest]
DJANGO_SETTINGS_MODULE = sannap_project.settings
python_files = tests.py test_*.py *_tests.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
```

## 💡 Testing Best Practices

### 1. Use Fixtures
```python
# Good
def test_with_fixture(authenticated_client):
    response = authenticated_client.get('/api/profile/')
    
# Avoid
def test_without_fixture():
    client = APIClient()
    user = User.objects.create(username='test')
    # ... manual setup
```

### 2. Test One Thing at a Time
```python
# Good
def test_register_success(api_client):
    response = api_client.post('/api/register/', data)
    assert response.status_code == 201

def test_register_returns_token(api_client):
    response = api_client.post('/api/register/', data)
    assert 'token' in response.data
```

### 3. Use Descriptive Names
```python
# Good
def test_user_cannot_delete_others_document(authenticated_client):
    pass

# Avoid
def test_delete(authenticated_client):
    pass
```

### 4. Arrange-Act-Assert Pattern
```python
def test_create_document(authenticated_client):
    # Arrange
    data = {'title': 'Test', 'content': 'Content'}
    
    # Act
    response = authenticated_client.post('/api/documents/', data)
    
    # Assert
    assert response.status_code == 201
    assert response.data['title'] == 'Test'
```

## 🐛 Debugging Tests

### Print Debug Information
```bash
pytest -s  # Show print statements
```

### Stop on First Failure
```bash
pytest -x
```

### Run Last Failed Tests
```bash
pytest --lf
```

### Drop into Debugger on Failure
```bash
pytest --pdb
```

## 📊 Continuous Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pytest --cov=. --cov-report=xml
      - uses: codecov/codecov-action@v2
```

## 📝 Writing New Tests

### 1. Create Test File
```bash
# In appropriate app/tests/ directory
touch myapp/tests/test_my_feature.py
```

### 2. Import Required Modules
```python
import pytest
from rest_framework import status
```

### 3. Write Test Class
```python
class TestMyFeature:
    def test_feature_works(self, authenticated_client):
        response = authenticated_client.get('/api/my-endpoint/')
        assert response.status_code == status.HTTP_200_OK
```

### 4. Run Your Tests
```bash
pytest myapp/tests/test_my_feature.py -v
```

## 🔗 Additional Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Django REST Framework Testing](https://www.django-rest-framework.org/api-guide/testing/)
- [Django Testing Documentation](https://docs.djangoproject.com/en/stable/topics/testing/)
- [Coverage.py Documentation](https://coverage.readthedocs.io/)
