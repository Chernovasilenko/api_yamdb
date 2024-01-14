from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

from django.db import models

from core import constants as const


class User(AbstractUser):
    """Модель кастомных пользователей."""

    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    ROLES = [
        (USER, 'user'),
        (ADMIN, 'admin'),
        (MODERATOR, 'moderator'),
    ]
    username = models.CharField(
        max_length=const.MAX_LENGHT_NAME_FIELD,
        unique=True,
        verbose_name='Имя пользователя',
        blank=False,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+\Z',
                message='Имя пользователя содержит недопустимые символы',
            )
        ]
    )
    first_name = models.CharField(
        max_length=const.MAX_LENGHT_NAME_FIELD,
        blank=True,
        verbose_name='Имя',
    )
    last_name = models.CharField(
        max_length=const.MAX_LENGHT_NAME_FIELD,
        blank=True,
        verbose_name='Фамилия',
    )
    email = models.EmailField(
        max_length=const.MAX_LENGHT_EMEIL_FIELD,
        unique=True,
        verbose_name='Электронная почта',
    )
    bio = models.TextField(
        blank=True,
        verbose_name='Биография'
    )
    role = models.CharField(
        max_length=const.MAX_STR_LENGTH,
        choices=ROLES,
        default='user',
        verbose_name='Роль',
    )

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    def __str__(self):
        return self.username[:const.MAX_STR_LENGTH]
