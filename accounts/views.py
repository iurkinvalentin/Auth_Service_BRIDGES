from rest_framework import generics
from .models import CustomUser, Profile
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from .serializers import UserSerializer, ProfileSerializer, LoginSerializer, RegisterSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView


class LoginView(APIView):
    """Вью для авторизации пользователя"""
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        """Обработка POST запроса для авторизации"""
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']  # Добавьте возврат пользователя в LoginSerializer
            token, created = Token.objects.get_or_create(user=user)
            return Response({'auth_token': token.key},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """Вью для выхода пользователя"""

    def post(self, request, *args, **kwargs):
        """Обработка POST запроса для выхода"""
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RegisterView(APIView):
    """Представление для страницы регистрации пользователя."""
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        """Обрабатывает запрос на регистрацию нового пользователя."""
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": (
                        "User registered successfully. "
                        "Please check your email for verification."
                    )
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
