from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import (
    RegexValidator, MaxValueValidator,
    MinValueValidator
)
from django.db import models
from django.utils import timezone

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


class AbstractModelGenreCategory(models.Model):
    """Абстрактная модель для жанров и категорий."""

    name = models.CharField(
        verbose_name='Название',
        max_length=const.MAX_LENGHT_CHAR_FIELD,
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        max_length=const.MAX_LENGHT_SLUG_FIELD,
        unique=True,
    )

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name[:const.MAX_STR_LENGTH]


class CommentReviewAbstractModel(models.Model):
    """Абстрактная модель для комментариев и отзывов."""

    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE
    )
    text = models.TextField('Введите текст')
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        abstract = True


class Genre(AbstractModelGenreCategory):
    """Модель для жанров."""

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        default_related_name = 'genres'


class Category(AbstractModelGenreCategory):
    """Модель для категорий."""

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        default_related_name = 'categories'


class Title(models.Model):
    """Модель для произведений."""

    name = models.CharField(
        verbose_name='Название',
        max_length=const.MAX_LENGHT_CHAR_FIELD,
    )
    year = models.PositiveSmallIntegerField(
        verbose_name='Год создания',
        validators=[
            MinValueValidator(
                limit_value=const.MIN_VALUE,
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
        through='GenreTitle',
        verbose_name='Жанр',
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True,
        blank=True
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name[:const.MAX_STR_LENGTH]


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title}: {self.genre}'[:const.MAX_STR_LENGTH]


class Review(CommentReviewAbstractModel):
    """Модель отзывов."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение для отзыва'
    )
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(
                const.MIN_VALUE,
                message='Оценка должна быть не меньше 1'
            ),
            MaxValueValidator(
                const.MAX_VALUE,
                message='Оценка должна быть не выше 10'
            ),
        ],
        verbose_name='Рейтинг',
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'], name='unique_review')]

    def __str__(self):
        return self.text[:const.MAX_STR_LENGTH]


class Comments(CommentReviewAbstractModel):
    """Модель для комментариев."""

    review = models.ForeignKey(
        Review,
        related_name='comments',
        on_delete=models.CASCADE,
        verbose_name='Комментируемый отзыв'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-pub_date']

    def __str__(self):
        return self.text[:const.MAX_STR_LENGTH]
