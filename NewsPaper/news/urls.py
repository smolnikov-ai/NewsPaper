from django.urls import path
from django.views.decorators.cache import cache_page

from .views import (PostsList, PostDetail, PostCreate, PostUpdate,
                    PostDelete, CategoryList, news_search,
                    subscribe,)

urlpatterns = [
    path('news/', cache_page(60*1)(PostsList.as_view()), name='post_list'),
    #path('news/', PostsList.as_view(), name='post_list'),
    #path('news/<int:pk>', cache_page(60*5)(PostDetail.as_view()), name='post_detail'),
    path('news/<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('news/search/', news_search, name='post_search'),
    path('news/create/', PostCreate.as_view(), name='news_create'),
    path('news/<int:pk>/edit/', PostUpdate.as_view(), name='news_edit'),
    path('news/<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
    path('articles/create/', PostCreate.as_view(), name='articles_create'),
    path('articles/<int:pk>/edit/', PostUpdate.as_view(), name='articles_edit'),
    path('articles/<int:pk>/delete/', PostDelete.as_view(), name='articles_delete'),
    path('category/<int:pk>/', CategoryList.as_view(), name='category_list'),
    path('category/<int:pk>/subscribe/', subscribe, name='category_subscribe'),
]