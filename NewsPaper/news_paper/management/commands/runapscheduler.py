import logging
import django.contrib.auth

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from news_paper.models import Post, Mailing
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from datetime import datetime, timedelta


logger = logging.getLogger(__name__)


def my_job():
    start_date = datetime.now().replace(hour=10, minute=0, second=0)
    end_date = start_date + timedelta(weeks=1)

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

            posts_list_txt = ', '.join([post.header for post in send_post])
            msg = EmailMultiAlternatives(
                subject='Список новых статей',
                body=f'Здравствуй, {person.username}.'
                f'Список новых статей за неделю:'
                f'{posts_list_txt}',
                from_email='sf.testmail@yandex.ru',
                to=[person.email],
            )
            msg.attach_alternative(html_content, "text/html")

            msg.send()


def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age`
    from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(second="*/20"),
            # my_job,
            # trigger=CronTrigger(
            #     day_of_week="mon", hour="10", minute="00"
            # ),
            id="my_job",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
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
