from django.core.management.base import BaseCommand
from news_paper.models import Post
from news_paper.models import Category


class Command(BaseCommand):
    help = 'Deleting all posts of specified category'

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        answer = input(f'Вы правда хотите удалить все статьи в категории'
                       f'{options["category"]}? yes/no')

        if answer != 'yes':
            self.stdout.write(self.style.ERROR('Отменено'))
        else:
            try:
                category = Category.objects.get(category=options['category'])
                Post.objects.filter(categories__category
                                    = category.category).delete()
                self.stdout.write(
                    self.style.SUCCESS(f'Succesfully deleted allposts from '
                                       f'category {category.category}')
                    )
            except Category.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Could not find category '
                                                   f'{options["category"]}'))
