from django.urls import path
from .views import IndexView
from .views import upgrade_me

urlpatterns = [
    path('index/', IndexView.as_view()),
    path('upgrade/', upgrade_me, name='upgrade'),
]