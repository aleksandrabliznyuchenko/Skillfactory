from django.core.management.base import BaseCommand
from news.models import Post, Category


class Command(BaseCommand):
    help = 'Команда, удаляющая все новости выбранной категории'

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        answer = input(f'Вы правда хотите удалить все статьи в категории {options["category"]}? yes/no')

        if answer != 'yes':
            self.stdout.write(self.style.ERROR('Отменено'))

        try:
            category = Category.get(name=options['category'])
            Post.objects.filter(category == category).delete()
            self.stdout.write(self.style.SUCCESS(
                f'Успешно удалены все новости из категории {category.name}'))
        except Post.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Новости в категории не найдены'))