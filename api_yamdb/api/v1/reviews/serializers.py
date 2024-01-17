from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from core import constants as const
from reviews.models import Category, Comments, Genre, Review, Title

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий."""

    class Meta:
        model = Category
        fields = ('name', 'slug',)


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров."""

    class Meta:
        model = Genre
        fields = ('name', 'slug',)


class TitleGetSerializer(serializers.ModelSerializer):
    """Сериализатор для получения произведений."""

    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'description', 'year', 'genre', 'category', 'rating'
        )
        read_only_fields = (
            'id', 'name', 'description', 'year', 'genre', 'category', 'rating'
        )


class TitleEditSerializer(serializers.ModelSerializer):
    """Сериализатор для редактирования произведений."""

    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'description', 'year', 'genre', 'category',
        )

    def validate_year(self, value):
        """Проверка допустимости значения года."""

        if (value > timezone.now().year):
            raise serializers.ValidationError(
                'Год произведения не может быть больше текущего!'
            )
        if (value < const.MIN_VALUE):
            raise serializers.ValidationError(
                'Год произведения не может быть ниже 1!'
            )
        return value


class AuthorMixin(serializers.Serializer):
    """Миксин автора."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )


class CommentSerializer(AuthorMixin, serializers.ModelSerializer):
    """Сериализатор комментариев."""

    class Meta:
        fields = '__all__'
        model = Comments
        read_only_fields = ('review', 'author')


class ReviewSerializer(AuthorMixin, serializers.ModelSerializer):
    """Сериализатор отзывов."""

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ('title', 'author')

        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('author', 'title'),
                message='Вы уже оставили отзыв!'
            )
        ]

    def to_internal_value(self, data):
        """Добавление произведения для последующей проверки в валидаторе."""
        data = super().to_internal_value(data)
        data['title'] = self.context['view'].title_for_reviews()
        return data
