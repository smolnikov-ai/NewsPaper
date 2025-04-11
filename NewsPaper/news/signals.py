'''
Performs the sending messages at the event - creation of a Post, to users subscribed in Category Post
Instead, a similar mailing list using Celery & Redis has been implemented.

Выполняет рассылку сообщений при событии - создание Post, пользователям подписанным на Category Post
Взамен реализована аналогичная рассылка с применением Celery & Redis
'''

#
# from django.conf import settings
# from django.core.mail import EmailMultiAlternatives
# from django.db.models.signals import m2m_changed
# from django.dispatch import receiver
# from django.template.loader import render_to_string
#
# #from NewsPaper import settings
# from news.models import PostCategory, Category
#
#
# def send_notifications(preview, pk, title, subscribers):
#     for s in subscribers:
#         html_content = render_to_string(
#             'post_created_email.html',
#             {
#                 'text': preview,
#                 'username': s.username,
#                 'link': f'{settings.SITE_URL}/news/{pk}',
#             }
#         )
#
#         msg = EmailMultiAlternatives(
#             subject=title,
#             body='',
#             from_email=settings.DEFAULT_FROM_EMAIL,
#             to=[s.email, ],
#         )
#
#         msg.attach_alternative(html_content, 'text/html')
#         msg.send()
#
#
# @receiver(m2m_changed, sender=PostCategory)
# def notify_about_new_post(sender, instance, **kwargs):
#     if kwargs['action'] == 'post_add':
#         categories = instance.categories.all()
#         subscribers = []
#
#         for cat in categories:
#             subscribers += cat.subscribers.all()
#
#         send_notifications(instance.preview(), instance.pk, instance.title, set(subscribers))
#
#
#
# # # отправка сообщения на почту username при добавлении новых статей на портал
# # # отправка происходит сразу списку пользователей
# # def send_notifications(preview, pk, title, subscribers):
# #     html_content = render_to_string(
# #         'post_created_email.html',
# #         {
# #             'text': preview,
# #             'link': f'{settings.SITE_URL}/news/{pk}',
# #         }
# #     )
# #
# #     msg = EmailMultiAlternatives(
# #         subject=title,
# #         body='',
# #         from_email=settings.DEFAULT_FROM_EMAIL,
# #         to=subscribers,
# #     )
# #
# #     msg.attach_alternative(html_content, 'text/html')
# #     msg.send()
# #
# #
# # @receiver(m2m_changed, sender=PostCategory)
# # def notify_about_new_post(sender, instance, **kwargs):
# #     if kwargs['action'] == 'post_add':
# #         categories = instance.categories.all()
# #         subscribers_emails = []
# #
# #         for cat in categories:
# #             subscribers = cat.subscribers.all()
# #             subscribers_emails += [s.email for s in subscribers]
# #
# #         send_notifications(instance.preview(), instance.pk, instance.title, subscribers_emails)