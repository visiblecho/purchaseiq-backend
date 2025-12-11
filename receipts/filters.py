import django_filters
from .models import Receipt
from django.db.models import Q


class ReceiptFilter(django_filters.FilterSet):
    # OR filter (any tag matches)
    tags_any = django_filters.CharFilter(method="filter_tags_any")

    # AND filter (all tags must match)
    tags_all = django_filters.CharFilter(method="filter_tags_all")

    # date range filters
    date_before = django_filters.DateFilter(field_name="datetime_parsed", lookup_expr="lte")
    date_after = django_filters.DateFilter(field_name="datetime_parsed", lookup_expr="gte")

    class Meta:
        model = Receipt
        fields = ["tags_any", "tags_all", "date_before", "date_after"]

    def filter_tags_any(self, queryset, name, value):
        """Matches any tag in the list (OR)."""
        tags = [tag.strip() for tag in value.split(",")]
        q = Q()
        for t in tags:
            q |= Q(items__tags__contains=[t])
        return queryset.filter(q).distinct()

    def filter_tags_all(self, queryset, name, value):
        """Matches all tags in the list (AND)."""
        tags = [tag.strip() for tag in value.split(",")]
        for t in tags:
            queryset = queryset.filter(items__tags__contains=[t])
        return queryset.distinct()
