from rest_framework import serializers


class ValidationUsernameMixin:

    def validate_username(self, username):
        """Проверка на допустимость имени пользователя."""
        if username == 'me':
            raise serializers.ValidationError(
                'Имя пользователя "me" запрещено.'
            )
        return username
