import csv

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from reviews.models import (
    Category, Comments, Genre, GenreTitle, Review, Title, User
)

DATA_DIR = f'{settings.BASE_DIR}\\static\\data\\'

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
    User: [
        'id', 'username', 'emeil', 'role', 'bio', 'first_name', 'last_name'
    ],
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
        with open(
                f'{DATA_DIR}{file_name}',
                'r',
                encoding='utf-8'
        ) as file:
            reader = csv.DictReader(file)
            try:
                model.objects.bulk_create(
                    model(**data) for data in reader)
            except ValueError as e:
                column_names = reader.fieldnames
                for row in column_names:
                    if row not in TABLES_ROWS[model]:
                        raise CommandError(
                            f'{e}\n'
                            f'Поля {row} нет в таблице. '
                            f'Проверьте названия полей в файле {file_name}. '
                            f'Допустимые поля: {TABLES_ROWS[model]}'
                        )
            finally:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Данные в таблицу {model.__qualname__} загружены'
                    )
                )

    def handle(self, *args, **options):
        try:
            for model, file_name in TABLES_FILES.items():
                self.load_data(model, file_name)
        except FileNotFoundError as e:
            raise CommandError(
                f'При загрузке данных в таблицу {model.__qualname__} '
                f'произошла ошибка {e}\n'
                f'Проверьте, что в директории "{DATA_DIR}" находится файл '
                f'"{file_name}" и он правильно назван'
            )
        except Exception as e:
            raise CommandError(
                f'При загрузке данных в таблицу {model.__qualname__} '
                f'произошла ошибка {e}\n'
            )
        finally:
            self.stdout.write(
                self.style.SUCCESS(
                    'Все данные успешно загружены'
                )
            )
