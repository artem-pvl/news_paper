from django.db import models
import django.contrib.auth

from django.dispatch import receiver
from django.db.models.signals import m2m_changed

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


class Author(models.Model):
    rating = models.IntegerField(default=0)
    user_id = models.OneToOneField(django.contrib.auth.get_user_model(),
                                   on_delete=models.CASCADE)

    def update_rating(self):
        posts_rate = 0
        posts_comments_rate = 0
        comments_rate = 0
        for p in Post.objects.filter(author=self):
            posts_rate += p.rating
            for pc in Comment.objects.filter(post=p.id):
                posts_comments_rate += pc.rating

        for ac in Comment.objects.filter(user=self.user_id):
            comments_rate += ac.rating

        self.rating = posts_rate*3 + posts_comments_rate + comments_rate
        self.save()


class Category(models.Model):
    category = models.CharField(max_length=255, unique=True)


class Post(models.Model):
    NEWS = 'N'
    ARTICLE = 'A'

    POST_TYPE = [
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(max_length=1, choices=POST_TYPE, default=ARTICLE)
    creation_time = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    header = models.CharField(max_length=255)
    text = models.TextField(default='')
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def priview(self):
        return self.text[:125] + ('...' if len(self.text) > 124 else '')


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Mailing(models.Model):
    subscribers = models.ForeignKey(django.contrib.auth.get_user_model(),
                                    on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


@receiver(m2m_changed, sender=PostCategory)
def do_mailing(sender, action, instance, **kwargs):
    if action == 'post_add':
        print(sender.objects.filter(post=instance.id).values('category'))
        category_lst = list(sender.objects.filter(post=instance.id).
                            values('category'))
        for category in category_lst:
            mailing_list = list(Mailing.objects.filter(
                category=category['category']).values('subscribers__username',
                                                      'subscribers__email'))
            print(category, mailing_list)
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


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(django.contrib.auth.get_user_model(),
                             on_delete=models.CASCADE)
    text = models.TextField(default='')
    creation_time = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
