from django_filters import rest_framework as filters
from .models import Manga


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class MovieFilter(filters.FilterSet):
    genres = CharFilterInFilter(field_name="genres__name", lookup_expr="in")
    published = filters.RangeFilter()

    class Meta:
        model = Manga
        fields = ("genres", "published")
