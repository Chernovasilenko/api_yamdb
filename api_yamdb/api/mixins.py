from rest_framework import mixins, viewsets
from rest_framework.filters import SearchFilter

from .permissions import AdminOrReadOnly


class GenreCategoryMixin(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """Миксин для жанров и категорий."""

    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    permission_classes = (AdminOrReadOnly,)
