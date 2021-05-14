from .models import PostCategory, Mailing

from django.dispatch import receiver
from django.db.models.signals import m2m_changed

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .tasks import send_mail


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

                send_mail.delay(instance.id, mail)
