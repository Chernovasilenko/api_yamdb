from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core import constants as const

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с пользователями."""

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )

    def validate_username(self, username):
        """Проверка на допустимость имени пользователя."""
        if username == 'me':
            raise serializers.ValidationError(
                'Имя пользователя "me" запрещено.'
            )
        return username


class UserCreateSerializer(serializers.Serializer):
    """Сериализатор для создания пользователя."""

    username = serializers.RegexField(
        max_length=const.MAX_LENGHT_NAME_FIELD,
        required=True,
        regex=r'^[\w.@+-]+\Z',
    )
    email = serializers.EmailField(
        max_length=const.MAX_LENGHT_EMEIL_FIELD,
        required=True
    )

    def validate_username(self, username):
        """Проверка на допустимость имени пользователя."""
        if username == 'me':
            raise serializers.ValidationError(
                'Имя пользователя "me" запрещено.'
            )
        return username

    def validate(self, data):
        """Проверка на доступность username и emeil."""
        email = data.get('email')
        username = data.get('username')
        if not User.objects.filter(username=username, email=email).exists():
            if User.objects.filter(username=username):
                raise ValidationError(
                    'Пользователь с таким именем уже существует'
                )
            if User.objects.filter(email=email):
                raise ValidationError('Пользователь с таким email существует')
        return data


class TokenSerializer(serializers.Serializer):
    """Сериализатор для получения токена пользователем."""
    username = serializers.CharField(
        max_length=const.MAX_LENGHT_NAME_FIELD,
        required=True
    )
    confirmation_code = serializers.CharField(required=True)
