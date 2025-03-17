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

    class Meta:
        model = Post
        fields = {
            'content': ['iregex'],
            'date_time_in': ['gt'],
            'author': ['exact'],
            # 'categories': ['exact'],
        }
