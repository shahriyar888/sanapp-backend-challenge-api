from drf_spectacular.utils import extend_schema
from ..serializers import RegisterSerializer, LoginSerializer, UserSerializer

# Schema definitions for account endpoints
REGISTER_SCHEMA = extend_schema(
    request=RegisterSerializer,
    responses={201: UserSerializer, 400: None}
)

LOGIN_SCHEMA = extend_schema(
    request=LoginSerializer,
    responses={200: UserSerializer, 400: None}
)

USER_PROFILE_SCHEMA = extend_schema(
    responses={200: UserSerializer}
)