import pytz

from django.utils import timezone

'''
Контекстный процессор передает значения переменных в любой шаблон
'''
def get_timezone(request):
    return {
        'current_timezone': timezone.now(),
        'timezones': pytz.common_timezones,
    }