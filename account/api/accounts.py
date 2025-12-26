from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from knox.models import AuthToken
from ..serializers import RegisterSerializer, LoginSerializer, UserSerializer
from ..docs.swagger_schemas import REGISTER_SCHEMA, LOGIN_SCHEMA, USER_PROFILE_SCHEMA


class RegisterView(APIView):
    permission_classes = [AllowAny]
    
    @REGISTER_SCHEMA
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
    permission_classes = [AllowAny]
    
    @LOGIN_SCHEMA
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

    @USER_PROFILE_SCHEMA
    def get(self, request):
        return Response(UserSerializer(request.user).data)