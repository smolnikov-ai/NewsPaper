from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


@shared_task()
def send_notifications(preview, pk, title, subscribers):
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