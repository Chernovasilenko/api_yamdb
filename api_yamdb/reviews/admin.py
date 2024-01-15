from django.contrib import admin

from reviews.models import Category, Comments, Genre, Review, Title


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
    

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'author', 'score',
                    'pub_date', 'title', 'title_id')
    search_fields = ('title', 'author')


@admin.register(Comments)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'author', 'pub_date', 'review', 'review_id')
    search_fields = ('author')


admin.site.site_title = 'Административный сайт YaMDb'
admin.site.site_header = 'Администрирование YaMDb'
admin.site.empty_value_display = 'Не задано'
