from .models import PostCategory, Mailing

from django.dispatch import receiver
from django.db.models.signals import m2m_changed

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


@receiver(m2m_changed, sender=PostCategory)
def do_mailing(sender, action, instance, **kwargs):
    if action == 'post_add':
        category_lst = list(sender.objects.filter(post=instance.id).
                            values('category'))
        for category in category_lst:
            mailing_list = list(Mailing.objects.filter(
                category=category['category']).values('subscribers__username',
                                                      'subscribers__email'))
            for mail in mailing_list:

                html_content = render_to_string(
                    'mailing.html',
                    {
                        'post': instance,
                        'text': instance.priview(),
                        'username': mail["subscribers__username"],
                    }
                )

                msg = EmailMultiAlternatives(
                    subject=f'{instance.header}',
                    body=f'Здравствуй, {mail["subscribers__username"]}. '
                    'Новая статья в твоём любимом разделе!',
                    from_email='sf.testmail@yandex.ru',
                    to=[mail['subscribers__email']],
                )
                msg.attach_alternative(html_content, "text/html")

                msg.send()
