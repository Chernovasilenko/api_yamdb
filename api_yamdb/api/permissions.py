from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class IsAdmin(permissions.BasePermission):
    """
    Cуперпользователи и администраторы имеют доступ к данным.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_admin
            or request.user.is_superuser
        )


class IsAdminOrReadOnly(IsAdmin):
    """
    Администратор или суперпользователь могут редактировать любые данные.
    Анонимный пользователь может запросить данные.
    """

    def has_permission(self, request, view):
        return super().has_permission or request.method in SAFE_METHODS


class IsModeratorOrAdminOrReadOnly(permissions.BasePermission):
    """
    Модератор или администратор может редактировать любые данные.
    Анонимный пользователь может запросить данные.
    """

    def has_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and (
            request.user.is_admin
            or request.user.is_moderator
            or obj.author == request.user
        )
