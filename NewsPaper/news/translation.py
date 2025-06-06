from .models import Category, Post
from modeltranslation.translator import register, TranslationOptions

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = ('author', 'type', 'categories', 'title', 'content', 'rating_post',)