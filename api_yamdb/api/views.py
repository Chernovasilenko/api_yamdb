from rest_framework import mixins, viewsets
from rest_framework.filters import SearchFilter

from reviews.models import Category, Genre, Title
from serializers import CategorySerializer, GenreSerializer, TitleSerializer


class GenreCategoryMixin(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """Миксин для жанров и категорий."""

    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    # добавить пермишен - админ или только чтение
    # permission_classes = (IsAdminOrReadOnly,)


class TitleViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для произведений.
    """
    # добавить в кверисет среднее значение через annotate
    queryset = Title.objects.annotate(rating=7)  # вместо 7 - AVG
    serializer_class = TitleSerializer
    filterset_fields = ('name',)
    ordering = ('name',)
    # добавить пермишен: админ или только чтение
    # permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleSerializer
        return TitleSerializer


class GenreViewSet(GenreCategoryMixin):
    """
    Вьюсет для жанров.
    """

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoriesViewSet(GenreCategoryMixin):
    """
    Вьюсет для категорий.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
