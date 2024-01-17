from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'role',
    )
    search_fields = ('username', 'email')
    ordering = ('username',)


admin.site.site_title = 'Административный сайт YaMDb'
admin.site.site_header = 'Администрирование YaMDb'
admin.site.empty_value_display = 'Не задано'
