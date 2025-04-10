import os
from celery import Celery

# Для запуска Celery на Windows используем команду
# celery -A NewsPaper worker -l INFO --pool=solo
# из ~\projects\git\news_portal\NewsPaper


# Связываем настройки Django с настройками Celery через переменную окружения
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')

# создаем экземпляр приложения Celery и устанавливаем для него файл конфигурации
app = Celery('NewsPaper')
# указываем пространство имен, чтобы Celery сам находил необходимые настройки в общем конфигурационном
# файле settings.py. Он их будет искать по шаблону "CELERY_***"
app.config_from_object('django.conf:settings', namespace = 'CELERY')

# указываем Celery автоматически искать задания в файлах tasks.py каждого приложения проекта
app.autodiscover_tasks()