import csv

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from reviews.models import (
    Category, Comments, Genre, GenreTitle, Review, Title, User
)

TABLES_FILES = {
    User: 'users.csv',
    Category: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
    Review: 'review.csv',
    Comments: 'comments.csv',
    GenreTitle: 'genre_title.csv',
}

TABLES_ROWS = {
    User: ['id', 'username', 'emeil', 'role', 'bio', 'first_name', 'last_name'],
    Category: ['id', 'name', 'slug'],
    Genre: ['id', 'name', 'slug'],
    Title: ['id', 'name', 'year', 'category_id'],
    Review: ['id', 'title_id', 'text', 'author_id', 'score', 'pub_date'],
    Comments: ['id', 'review_id', 'text', 'author_id', 'pub_date'],
    GenreTitle: ['id', 'title_id', 'genre_id'],
}


class Command(BaseCommand):
    help = """Импорт данных из CSV-файлов для базы данных"""

    def load_data(self, model, file_name):
        file_path = f'{settings.BASE_DIR}/static/data/{file_name}'
        with open(
                file_path,
                'r',
                encoding='utf-8'
        ) as file:
            reader = csv.DictReader(file)
            try:
                model.objects.bulk_create(
                    model(**data) for data in reader)
            except ValueError as e:
                list_reader = list(csv.reader(file))
                print(reader.writeheader())
                print(list(csv.reader(file))[0])
                for row in (list(csv.reader(file))[0]):
                    if row not in TABLES_ROWS[model]:
                        self.stdout.write(self.style.ERROR(
                            f'Ошибка при загрузке данных в таблицу {model.__qualname__},'
                            f'Поля {row} нет в таблице. Допустимые поля:'
                            f'{TABLES_ROWS[model]}'
                        )
                        )
                        raise CommandError(
                                f'При загрузке данных в таблицу {model.__qualname__} произошла ошибка {e}'
                            )
                    else:
                        raise CommandError(
                            f'При загрузке данных в таблицу {model.__qualname__} произошла ошибка {e}'
                        )
            else:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Данные в таблицу {model.__qualname__} загружены'
                    )
                )

    def handle(self, *args, **options):
        for model, file_name in TABLES_FILES.items():
            self.load_data(model, file_name)
