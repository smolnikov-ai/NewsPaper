from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    content = forms.CharField()

    class Meta:
        model = Post
        fields = [
            'author',
            'type',
            'categories',
            'title',
            'content',
        ]
