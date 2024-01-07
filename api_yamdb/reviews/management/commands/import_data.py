import csv

from django.core.management import BaseCommand


FILES = (
    'category.csv',
    'comments.csv',
    'genre.csv',
    'genre_title.csv',
    'review.csv',
    'titles.csv',
    'users.csv',
)


class Command(BaseCommand):

    help = 'Импорт данных из файла CSV в базу данных'

    def handle(self, *args, **options):
        pass
