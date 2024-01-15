# Generated by Django 3.2 on 2024-01-15 11:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'default_related_name': 'categories', 'ordering': ('name',), 'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='genre',
            options={'default_related_name': 'genres', 'ordering': ('name',), 'verbose_name': 'Жанр', 'verbose_name_plural': 'Жанры'},
        ),
    ]
