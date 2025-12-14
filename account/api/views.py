from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from knox.models import AuthToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ..serializers import RegisterSerializer, LoginSerializer, UserSerializer


class RegisterView(APIView):
    @swagger_auto_schema(
        request_body=RegisterSerializer,
        responses={201: openapi.Response('User created', UserSerializer)}
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = AuthToken.objects.create(user)[1]
            return Response({
                'user': UserSerializer(user).data,
                'token': token
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={200: openapi.Response('Login successful', UserSerializer)}
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token = AuthToken.objects.create(user)[1]
            return Response({
                'user': UserSerializer(user).data,
                'token': token
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: UserSerializer}
    )
    def get(self, request):
        return Response(UserSerializer(request.user).data)