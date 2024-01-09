from django.core.mail import send_mail
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import TitleFilter
from .mixins import GenreCategoryMixin
from .permissions import (
    IsAdmin,
    IsAdminOrReadOnly,
    IsModeratorOrAdminOrReadOnly
)
from .serializers import (
    CategorySerializer, GenreSerializer,
    TitleGetSerializer, TitleEditSerializer,
    UserSerializer, CreateUserSerializer
)
from reviews.models import Category, Genre, Title, User


class UserViewSet(viewsets.GenericViewSet,
                  mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin
                  ):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)

    @action(detail=False,
            methods=['get', 'patch'],
            permission_classes=(permissions.IsAuthenticated,))
    def get_user_data(self, request):
        """
        Метод для получения данных пользователя и редактирования.
        """
        if request.method == 'GET':
            serializer = UserSerializer(self.request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(self.request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False,
            methods=['post'],
            permission_classes=(permissions.AllowAny,))
    def make_token(request):
        confirmation_code = PasswordResetTokenGenerator().make_token(request.user)
        return Response(
            {'confirmation_code': confirmation_code},
            status=status.HTTP_200_OK
        )

    def check_token(request):
        confirmation_code = request.data.get('confirmation_code')
        if confirmation_code is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if not PasswordResetTokenGenerator().check_token(request.user, confirmation_code):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)


class SignUpViewSet(viewsets.GenericViewSet,
                    mixins.CreateModelMixin
                    ):

    permission_classes = (permissions.AllowAny,)

    @action(detail=False,
            methods=['post'])
    def sign_up(self, request):
        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        email = serializer.validated_data['email']
        user, confirmation_code = User.objects.get_or_create(username=username, email=email)
        confirmation_code = PasswordResetTokenGenerator().make_token(user)
        send_mail(
            'Код подтверждения',
            f'{confirmation_code}',)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CheckConfirmationCode(viewsets.GenericViewSet,
                            mixins.CreateModelMixin
                            ):

    permission_classes = (permissions.AllowAny,)

    @action(detail=False,
            methods=['post'])
    def check_code(self, request):
        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        email = serializer.validated_data['email']
        user = get_object_or_404(User, username=username, email=email)
        confirmation_code = serializer.validated_data['confirmation_code']
        if not PasswordResetTokenGenerator().check_token(user, confirmation_code):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)


class GenreViewSet(GenreCategoryMixin):
    """Вьюсет для жанров."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(GenreCategoryMixin):
    """Вьюсет для категорий."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для произведений."""

    # здесь в кверисет должно добавиться значение rating,
    # которое берётся из среднего всех оценок из отзывов,
    # надеюсь будет работать как задумано
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    ordering = ('name',)
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        """Выбор сериализатора в зависимости от типа запроса."""

        if self.request.method == 'GET':
            return TitleGetSerializer
        return TitleEditSerializer
