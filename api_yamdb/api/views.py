from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import render, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets
from rest_framework.response import Response

from .filters import TitleFilter
from .mixins import GenreCategoryMixin
from .permissions import (
    AdminUser,
    AdminOrReadOnly,
    ModeratorOrAdminOrReadOnly,
    Owner
)
from .serializers import (
    CategorySerializer, GenreSerializer,
    TitleGetSerializer, TitleEditSerializer,
    UserSerializer, CreateUserSerializer
)
from reviews.models import Category, Genre, Title, User


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AdminUser, permissions.IsAuthenticated]


class GenreViewSet(GenreCategoryMixin):
    """Вьюсет для жанров."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(GenreCategoryMixin):
    """Вьюсет для категорий."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для произведений."""

    # здесь в кверисет должно добавиться значение rating,
    # которое берётся из среднего всех оценок из отзывов,
    # надеюсь будет работать как задумано
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    ordering = ('name',)
    permission_classes = (AdminOrReadOnly,)

    def get_serializer_class(self):
        """Выбор сериализатора в зависимости от типа запроса."""

        if self.request.method == 'GET':
            return TitleGetSerializer
        return TitleEditSerializer
