from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone

from core import constants


class AbstractModelGenreCategory(models.Model):
    """Абстрактная модель для жанров и категорий."""

    name = models.CharField(
        verbose_name='Название',
        max_length=constants.MAX_LENGHT_CHAR_FIELD,
    )
    slug = models.SlugField(
        max_length=constants.MAX_LENGHT_SLUG_FIELD,
        unique=True,
    )

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name[:constants.MAX_TITLE_LENGTH]


class Genre(AbstractModelGenreCategory):
    """Модель для жанров."""

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        default_related_name = 'genres'


class Category(models.Model):
    """Модель для категорий."""

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        default_related_name = 'categories'


class Title(models.Model):
    """Модель для произведений."""

    name = models.CharField(
        verbose_name='Название',
        max_length=constants.MAX_LENGHT_CHAR_FIELD,
    )
    year = models.PositiveSmallIntegerField(
        verbose_name='Год',
        validators=[
            MinValueValidator(
                limit_value=constants.MIN_YEAR,
                message='Год выпуска не может быть меньше или равен нулю!'
            ),
            MaxValueValidator(
                limit_value=timezone.now().year,
                message='Год выпуска не может быть больше текущего!'
            )
        ]
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
        ordering = ('name',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name[:constants.MAX_TITLE_LENGTH]
