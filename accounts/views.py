from rest_framework import generics
from .models import CustomUser, Profile
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from .serializers import UserSerializer, ProfileSerializer, LoginSerializer
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
            user = serializer.validated_data
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