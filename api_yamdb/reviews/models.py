from django.contrib.auth.models import AbstractUser
from django.db import models


ROLES = [
    ('anonymous', 'Аноним'),
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
]


class Genre(models.Model):
    """Модель для жанра."""

    name = models.CharField(
        verbose_name='Название',
        max_length=256,
    )
    slug = models.SlugField(
        max_length=256,
        unique=True,
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Category(models.Model):
    """Модель для категорий."""

    name = models.CharField(
        verbose_name='Название',
        max_length=256,
    )
    slug = models.SlugField(
        max_length=256,
        unique=True,
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель для произведений."""

    name = models.CharField(
        verbose_name='Название',
        max_length=256,
    )
    year = models.PositiveSmallIntegerField(
        verbose_name='Год',
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='titles',
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class User(AbstractUser):
    """Модель кастомных пользователей."""

    first_name = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Имя',
    )
    last_name = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Фамилия',
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Электронная почта',
    )
    bio = models.TextField(
        blank=True,
        verbose_name='Биография',
    )
    role = models.CharField(
        max_length=100,
        choices=ROLES,
        default='user',
        verbose_name='Роль',
    )
    confirmation_code = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Код подтверждения',
    )

    def __str__(self):
        return self.username
