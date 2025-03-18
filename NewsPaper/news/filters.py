import django_filters
from django.forms import DateInput
from django_filters import FilterSet, ModelChoiceFilter
from .models import Post, Category, Author


class PostFilter(FilterSet):
    author = ModelChoiceFilter(
        field_name='author',
        queryset=Author.objects.all(),
        label='Author',
        empty_label='Любой',
    )

    category = ModelChoiceFilter(
        field_name='postcategory__category',
        queryset=Category.objects.all(),
        label='Category',
        empty_label='Любая',
    )

    date_time_in = django_filters.DateFilter(
        widget=DateInput(attrs={'type': 'date', 'field': 'date_time'}),
        lookup_expr='date__gte',
        label='Даты выхода'
    )

    class Meta:
        model = Post
        fields = {
            'content': ['iregex'],
            'type':['exact'],
        }
