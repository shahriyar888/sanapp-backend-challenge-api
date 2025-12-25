# Test Suite

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run all tests:
```bash
pytest
```

3. Run specific test file:
```bash
pytest account/tests/test_register_view.py
pytest account/tests/test_login_view.py
pytest account/tests/test_user_profile_view.py
pytest document/tests/test_document_viewset.py
```

4. Run with coverage:
```bash
pytest --cov=. --cov-report=html
```

## Test Structure

- `conftest.py` - Reusable fixtures (users, auth, documents)
- `account/tests/` - Account app tests
  - `test_register_view.py` - RegisterView (201, 400)
  - `test_login_view.py` - LoginView (200, 400)
  - `test_user_profile_view.py` - UserProfileView (200, 401)
- `document/tests/` - Document app tests
  - `test_document_viewset.py` - DocumentViewSet (200, 201, 204, 400, 401, 404)

## Fixtures

- `api_client` - Unauthenticated API client
- `user` - Basic user instance
- `user_with_password` - User with password set
- `auth_token` - Knox authentication token
- `authenticated_client` - Authenticated API client
- `document` - Document instance
