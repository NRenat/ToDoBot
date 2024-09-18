import django_filters
from .models import Task


class TaskFilter(django_filters.FilterSet):
    id = django_filters.CharFilter(field_name="id", lookup_expr="exact")
    author = django_filters.CharFilter(field_name="author", lookup_expr="exact")
    completed = django_filters.BooleanFilter(field_name="completed",
                                             lookup_expr="exact")

    class Meta:
        model = Task
        fields = ('id', 'author', 'completed')
