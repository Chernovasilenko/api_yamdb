from rest_framework import serializers
from django.core.validators import RegexValidator

from reviews.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'role',
        )


class CreateUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'role',
        )
        validators = [
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message=(
                    'Недопустимые символы в имени пользователя!'
                )
            )
        ]

    def validate_new_user(self, data):
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError(
                'Пользователь с таким именем уже существует.'
            )
        return data

    # Нужна ли здесь проверка на уникальность email?
    # На мой взгляд мы должны предусмотреть создание пользователя
    # с уникальным email.
    def validate(self, data):
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError(
                'Пользователь с таким email уже существует.'
            )
        return data
