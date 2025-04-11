import os
from celery import Celery
from celery.schedules import crontab

# Для запуска Celery на Windows используем команду
# celery -A NewsPaper worker -l INFO --pool=solo
# а для запуска периодических задач ещё в третьем терминале команду
# celery -A NewsPaper beat -l INFO
# из ~\projects\git\news_portal\NewsPaper


# Связываем настройки Django с настройками Celery через переменную окружения
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')

# создаем экземпляр приложения Celery и устанавливаем для него файл конфигурации
app = Celery('NewsPaper')
# указываем пространство имен, чтобы Celery сам находил необходимые настройки в общем конфигурационном
# файле settings.py. Он их будет искать по шаблону "CELERY_***"
app.config_from_object('django.conf:settings', namespace = 'CELERY')

# настройки для периодических задач
app.conf.beat_schedule = {
    'send_mail_with_posts_8am_monday': {
        'task': 'news.tasks.send_out_weekly',
        'schedule': crontab(minute=0, hour=8, day_of_week='monday'),
    },
}

# указываем Celery автоматически искать задания в файлах tasks.py каждого приложения проекта
app.autodiscover_tasks()