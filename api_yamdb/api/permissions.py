from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class AdminUser(permissions.BasePermission):
    """
    Cуперпользователи и администраторы имеют доступ к данным.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_admin
            or request.user.is_superuser
        )


class AdminOrReadOnly(permissions.BasePermission):
    """
    Администратор или суперпользователь могут редактировать любые данные.
    Анонимный пользователь может запросить данные.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and (
            request.user.is_admin
            or request.user.is_superuser
        )


class ModeratorOrAdminOrReadOnly(permissions.BasePermission):
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
        )


class Owner(permissions.BasePermission):
    """
    Владелец может редактировать только свои данные.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
