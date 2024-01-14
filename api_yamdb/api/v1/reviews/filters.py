from django_filters import CharFilter, FilterSet

from reviews.models import Title


class TitleFilter(FilterSet):
    """Фильтр для произведений."""

    category = CharFilter(field_name='category__slug')
    genre = CharFilter(field_name='genre__slug')
    name = CharFilter(field_name='name', lookup_expr='contains')

    class Meta:
        model = Title
        fields = ('name', 'category', 'genre', 'year')
