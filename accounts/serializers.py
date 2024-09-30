from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser, Profile, Connection
from django.core.validators import RegexValidator
from django.db import IntegrityError


class LoginSerializer(serializers.Serializer):
    """Сериализатор для авторизации пользователя"""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """Валидация учетных данных"""
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid credentials")


class RegisterSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователя"""
    email = serializers.EmailField(required=True)
    username = serializers.CharField(
        max_length=150,
        validators=[RegexValidator(r'^[\w.@+-]+$')],
        required=True
    )
    first_name = serializers.CharField(max_length=150, required=True)
    last_name = serializers.CharField(max_length=150, required=True)
    password = serializers.CharField(
        write_only=True, required=True,
        style={'input_type': 'password'})

    class Meta:
        model = CustomUser
        fields = ['username', 'id', 'email',
                  'password', 'first_name', 'last_name']

    def create(self, validated_data):
        """Создание нового пользователя"""
        try:
            user = CustomUser.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                first_name=validated_data.get('first_name', ''),
                last_name=validated_data.get('last_name', ''),
                password=validated_data['password']
            )
        except IntegrityError:
            raise serializers.ValidationError(
                {
                    "username": (
                        "Пользователь с такими данными уже существует"
                    )
                }
            )
        return user


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('username', 'id', 'email', 'first_name', 'last_name')


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ('user', 'avatar', 'status_message', 'is_online', 'last_seen')


class FriendshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connection
        fields = ('from_user', 'to_user', 'created')