from django.core.management.base import BaseCommand
from reviews.models import (
    Category, Comments, Genre, GenreTitle, Review, Title, User
)


class Command(BaseCommand):

    def handle(self, *args, **options):
        print(GenreTitle._meta.get_fields())
