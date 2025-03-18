from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    content = forms.CharField()

    class Meta:
        model = Post
        fields = [
            'author',
            'categories',
            'title',
            'content',
        ]


class NewsSearchForm(forms.Form):
    title = forms.CharField(label='Название', required=False)
    author = forms.CharField(label='Автор', required=False)
    date_after = forms.DateField(label='Позже даты', required=False,
                                 widget=forms.DateInput(attrs={'type': 'date'}))  # Указываем тип для HTML5

    def clean_date_after(self):  # Если нужно, добавляем валидацию даты
        date_after = self.cleaned_data.get('date_after')
        return date_after
