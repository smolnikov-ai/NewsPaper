from django.contrib import admin
from .models import Post, Category


# создаем новый класс для представления товаров в admin panel
class PostAdmin(admin.ModelAdmin):
    # list_display - это список или кортеж с полями, которые будут отображаться в таблице в admin panel
    list_display = ['title','date_time_in', 'author',]
    # list_filter - примитивные фильтра в админке
    list_filter = ['categories', 'author', 'type',]
    # search_fields - поиск по указанным полям
    search_fields =  ['title', 'content']


# регистрация моделей
admin.site.register(Post, PostAdmin)
admin.site.register(Category)
