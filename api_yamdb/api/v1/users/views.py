from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view, action
from rest_framework import viewsets, status
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from . import serializers
from .. import permissions

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с пользователями."""

    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.IsAdmin,)
    filter_backends = (SearchFilter,)
    lookup_field = 'username'
    search_fields = ('username',)
    http_method_names = ('get', 'post', 'patch', 'delete')

    @action(detail=False,
            methods=('get', 'patch'),
            url_path='me',
            url_name='me',
            permission_classes=(IsAuthenticated,))
    def get_user_data(self, request):
        """Получение и редактирование данных пользователя."""
        if request.method == 'PATCH':
            serializer = serializers.UserSerializer(
                request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = serializers.UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(('POST',))
def sign_up(request):
    """Создание пользователя."""
    serializer = serializers.CreateUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    email = serializer.validated_data['email']
    user, confirmation_code = User.objects.get_or_create(
        username=username,
        email=email
    )
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject='Код подтверждения',
        message=f'Ваш код подтверждения: {confirmation_code}',
        from_email='yamdb_email@yamdb.ru',
        recipient_list=(email,),
        fail_silently=False
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(('POST',))
def check_code(request):
    """Создание JWT-токена."""
    serializer = serializers.TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    user = get_object_or_404(User, username=username)
    confirmation_code = serializer.validated_data['confirmation_code']
    if not default_token_generator.check_token(user, confirmation_code):
        return Response(
            {'confirmation_code': 'Неверный код подтверждения'},
            status=status.HTTP_400_BAD_REQUEST
        )
    return Response(
        {'token': str(AccessToken.for_user(user))},
        status=status.HTTP_200_OK
    )
