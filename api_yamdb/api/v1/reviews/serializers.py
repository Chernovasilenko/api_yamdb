from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from core import constants as const
from reviews.models import Category, Comments, Genre, Title, Review

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

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

    def validate(self, data):
        if data.get('username') == 'me':
            raise serializers.ValidationError(
                'Имя пользователя "me" запрещено.'
            )
        return data


class CreateUserSerializer(serializers.Serializer):
    username = serializers.RegexField(
        max_length=const.MAX_LENGHT_NAME_FIELD,
        required=True,
        regex=r'^[\w.@+-]+\Z',
    )
    email = serializers.EmailField(
        max_length=const.MAX_LENGHT_EMEIL_FIELD,
        required=True
    )

    def validate(self, data):
        if data.get('username') == 'me':
            raise serializers.ValidationError(
                'Имя пользователя "me" запрещено.'
            )
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
    username = serializers.CharField(
        max_length=const.MAX_LENGHT_NAME_FIELD,
        required=True
    )
    confirmation_code = serializers.CharField(required=True)


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
    rating = serializers.IntegerField()  #

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
    rating = serializers.IntegerField(required=False)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'description', 'year', 'genre', 'category', 'rating'
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


class AuthorSerializer(serializers.ModelSerializer):
    """Сериализатор автора."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )


class CommentSerializer(AuthorSerializer):
    """Сериализатор комментариев."""

    class Meta:
        fields = '__all__'
        model = Comments
        read_only_fields = ('review', 'author')


class ReviewSerializer(AuthorSerializer):
    """Сериализатор отзывов."""

    def validate(self, data):
        """Валидация отзыва."""
        request = self.context['request']
        author = request.user
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if (
            request.method == 'POST'
            and title.reviews.filter(author=author).exists()
        ):
            raise ValidationError('Вы уже оставили отзыв!')
        return data

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ('title', 'author')
