from django.urls import path
from .views import PostsList, PostDetail, PostCreate, PostUpdate, PostDelete, news_search

urlpatterns = [
    path('news/', PostsList.as_view(), name='post_list'),
    path('news/<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('news/search/', news_search, name='post_search'),
    path('news/create/', PostCreate.as_view(), name='news_create'),
    path('news/<int:pk>/edit/', PostUpdate.as_view(), name='news_edit'),
    path('news/<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
    path('articles/create/', PostCreate.as_view(), name='articles_create'),
    path('articles/<int:pk>/edit/', PostUpdate.as_view(), name='articles_edit'),
    path('articles/<int:pk>/delete/', PostDelete.as_view(), name='articles_delete'),
]