from django.contrib import admin
from django.contrib.auth import get_user_model

from reviews.models import Category, Genre, Comments, Review, Title

User = get_user_model()


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'year', 'category', 'description')
    search_fields = ('name',)
    raw_id_fields = ('category', 'genre')
    ordering = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(User)
admin.site.register(Review)
admin.site.register(Comments)

admin.site.site_title = 'Административный сайт YaMDb'
admin.site.site_header = 'Администрирование YaMDb'
admin.site.empty_value_display = 'Не задано'
