'''
Performs the distribution of weekly messages, and messages at the event - the creation of a post.
The file is being used 'news/signals.py' and a second Terminal for the command 'python manage.py runapscheduler'.
Instead, a similar mailing list using Celery & Redis has been implemented.

Выполняет рассылку еженедельных сообщений, и сообщений при событии - создание поста.
Используется файл 'news/signals.py' и второй Terminal для команды 'python manage.py runapscheduler'.
Взамен реализована аналогичная рассылка с применением Celery & Redis
'''

import datetime
import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from news.models import Post, Category

logger = logging.getLogger(__name__)


# наша задача по выводу текста на экран
def my_job():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(date_time_in__gte=last_week)
    categories = set(posts.values_list('categories__name', flat=True))

    # строка определения первичного ключа для рассылки отдельно каждому юзеру через цикл
    subscribers_pk = set(Category.objects.filter(name__in=categories).values_list('subscribers__pk', flat=True))

    # рассылка сообщений циклом каждому username отдельно
    for pk in subscribers_pk:
        user = User.objects.get(id=pk)

        # создаем context для передачи в html шаблон
        # в частности нужный нам username каждого пользователя, кому уходит письмо
        html_content = render_to_string(
            'daily_post.html',
            {
                'link': settings.SITE_URL,
                'username': user.username,
                'posts': posts,
            }
        )

        msg = EmailMultiAlternatives(
            subject='Статьи прошедшей недели',
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email, ],
        )

        msg.attach_alternative(html_content, 'text/html')
        msg.send()


    # строка с почтами подписчиков для отправки сообщений списку пользователей
    #subscribers = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))

    # рассылка сообщений списку пользователей
    # html_content = render_to_string(
    #     'daily_post.html',
    #     {
    #         'link': settings.SITE_URL,
    #         'username': user.username,
    #         'posts': posts,
    #     }
    # )
    # msg = EmailMultiAlternatives(
    #     subject='Статьи прошедшей недели',
    #     body='',
    #     from_email=settings.DEFAULT_FROM_EMAIL,
    #     to=subscribers,
    # )

    # msg.attach_alternative(html_content, 'text/html')
    # msg.send()


# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            # default запуск каждую минуту
            # trigger=CronTrigger(second="*/59"),
            trigger=CronTrigger(second="*/10"),
            # запуск по дню недели и времени
            #trigger=CronTrigger(day_of_week='thu', hour='20', minute='34'),
            # То же, что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")