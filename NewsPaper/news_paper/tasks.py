from celery import shared_task

import django.contrib.auth
from .models import Post, Mailing
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.translation import gettext

from datetime import datetime, timedelta


@shared_task
def send_mail(post_id, mailing):
    post = Post.objects.get(id=post_id)

    html_content = render_to_string(
        'mailing.html',
        {
            'post': post,
            'text': post.priview(),
            'username': mailing["subscribers__username"],
        }
    )

    msg = EmailMultiAlternatives(
        subject=f'{post.header}',
        body=gettext(
            'Hello, %(name)s. New articles in your favorite category!') % {
                    'name': mailing["subscribers__username"]
                },
        from_email='sf.testmail@yandex.ru',
        to=[mailing['subscribers__email']],
    )
    msg.attach_alternative(html_content, "text/html")

    msg.send()


@shared_task
def do_mailing():
    end_date = datetime.now().replace(hour=8, minute=0, second=0)
    start_date = end_date - timedelta(weeks=1)

    for person in django.contrib.auth.get_user_model().objects.all():
        send_post = Post.objects.filter(
            creation_time__range=(start_date, end_date),
            categories__in=Mailing.objects.filter(subscribers=person).
            values('category')
            )
        if send_post:
            html_content = render_to_string(
                'mailing_list.html',
                {
                    'post': send_post,
                    'user': person,
                }
            )

            msg_text = gettext(
                'Hello, %(name)s. New articles for the week:'
            ) % {'name': person.username}

            posts_list_txt = ', '.join([post.header for post in send_post])

            msg = EmailMultiAlternatives(
                subject=gettext('New articles list'),
                body=msg_text+'\n'+posts_list_txt,
                # body=f'Здравствуй, {person.username}.'
                # f'Список новых статей за неделю:'
                # f'{posts_list_txt}',
                from_email='sf.testmail@yandex.ru',
                to=[person.email],
            )
            msg.attach_alternative(html_content, "text/html")

            msg.send()
