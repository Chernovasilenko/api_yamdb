from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets

from . import serializers
from .. import permissions
from .filters import TitleFilter
from .mixins import GenreCategoryMixin
from reviews.models import Category, Genre, Title, Review


class GenreViewSet(GenreCategoryMixin):
    """Вьюсет для жанров."""

    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer


class CategoryViewSet(GenreCategoryMixin):
    """Вьюсет для категорий."""

    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для произведений."""

    http_method_names = ('get', 'post', 'patch', 'delete')
    permission_classes = (permissions.IsAdminOrReadOnly,)
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        """Выбор сериализатора в зависимости от типа запроса."""
        if self.request.method == 'GET':
            return serializers.TitleGetSerializer
        return serializers.TitleEditSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет отзывов."""

    serializer_class = serializers.ReviewSerializer
    permission_classes = (permissions.IsModeratorOrAdminOrReadOnly,)
    http_method_names = ('get', 'post', 'patch', 'delete')

    def title_for_reviews(self):
        """Получение объекта произведения."""
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        """Запрос отзывов на произведение."""
        return self.title_for_reviews().reviews.all()

    def perform_create(self, serializer):
        """Создание отзыва с сохранением автора и произведения."""
        serializer.save(
            author=self.request.user,
            title=self.title_for_reviews()
        )


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет комментариев."""

    serializer_class = serializers.CommentSerializer
    permission_classes = (permissions.IsModeratorOrAdminOrReadOnly,)
    http_method_names = ('get', 'post', 'patch', 'delete')

    def commented_review(self):
        """Получение объекта комментария."""
        return get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'),
            title=self.kwargs.get('title_id')
        )

    def get_queryset(self):
        """Запрос комментариев на отзыв."""
        return self.commented_review().comments.all()

    def perform_create(self, serializer):
        """Создание комментария с сохранением автора и отзыва."""
        serializer.save(
            author=self.request.user,
            review=self.commented_review()
        )
