import datetime

from celery import shared_task
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from news.models import Category, Post

# задача рассылки писем подписчикам по событию
@shared_task()
def send_notifications_subscribers_categories(preview, pk, title, subscribers):
    for s in subscribers:
        html_content = render_to_string(
            'post_created_email.html',
            {
                'text': preview,
                'username': s.username,
                'link': f'{settings.SITE_URL}/news/{pk}',
            }
        )

        msg = EmailMultiAlternatives(
            subject=title,
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[s.email, ],
        )

        msg.attach_alternative(html_content, 'text/html')
        msg.send()

# задача еженедельной отправки сообщений подписчикам
@shared_task()
def send_out_weekly():
    # определяем сегодняшний день, который соответствует полю schedule в NewsPaper/celery.py
    today = datetime.datetime.now()
    # определяем день (и время) на неделю ранее today
    last_week = today - datetime.timedelta(days=7)
    # определяем список объектов модели Post >= (свежее) last_week
    posts = Post.objects.filter(date_time_in__gte=last_week)
    # определяем список объектов модели Category соответствующих posts, через связь ManyToMany
    # так как повторы нам не нужны, оборачиваем в множество - set()
    categories = set(posts.values_list('categories__name', flat=True))
    # определяем список объектов модели User соответствующих categories, через связь ManyToMany
    # так как повторы нам не нужны, оборачиваем в множество - set()
    subscribers = set(Category.objects.filter(name__in=categories).values_list('subscribers', flat=True))

    for pk in subscribers:
        s = User.objects.get(pk=pk)
        html_content = render_to_string(
            'daily_post.html',
            {
                'link': settings.SITE_URL,
                'username': s.username,
                'posts': posts,
            }
        )

        msg = EmailMultiAlternatives(
            subject='Статьи прошедшей недели',
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[s.email, ],
        )

        msg.attach_alternative(html_content, 'text/html')
        msg.send()