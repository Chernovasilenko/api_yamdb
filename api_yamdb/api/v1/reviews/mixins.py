from rest_framework import mixins, viewsets
from rest_framework.filters import SearchFilter

from ..permissions import IsAdminOrReadOnly


class GenreCategoryMixin(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """Миксин для жанров и категорий."""

    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)


class PatchModelMixin(
    mixins.UpdateModelMixin,
):
    """Миксин без PUT-запроса."""

    def partial_update(self, request, *args, **kwargs):
        if request.method == 'PATCH':
            return super().partial_update(request, *args, **kwargs)
        else:
            self.permission_denied()
