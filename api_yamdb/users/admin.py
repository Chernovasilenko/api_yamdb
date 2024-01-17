from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'role',
    )


admin.site.site_title = 'Административный сайт YaMDb'
admin.site.site_header = 'Администрирование YaMDb'
admin.site.empty_value_display = 'Не задано'
