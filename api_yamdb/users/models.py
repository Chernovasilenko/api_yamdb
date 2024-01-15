from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
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
        default=USER,
        verbose_name='Роль',
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_user'
            )
        ]

    def clean(self):
        super().clean()
        if self.username == 'me':
            raise ValidationError(
                'Имя пользователя "me" запрещено.'
            )

    def __str__(self):
        return self.username[:const.MAX_STR_LENGTH]

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR
