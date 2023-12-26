from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from rest_framework import (
    permissions,
    viewsets
)
from rest_framework.response import Response

from .permissions import (
    AdminUser,
    AdminOrReadOnly,
    ModeratorOrAdminOrReadOnly,
    Owner
)
from .serializers import (
    UserSerializer,
    CreateUserSerializer
)
from reviews.models import User


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AdminUser, permissions.IsAuthenticated]
    lookup_field = 'username'
