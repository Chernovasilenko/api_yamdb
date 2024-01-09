from django.core.mail import send_mail
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import permissions, viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.views import APIView

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
    UserSerializer, CreateUserSerializer,
    ReviewSerializer, CommentSerializer,
)
from reviews.models import Category, Genre, Title, Review, User


class UserViewSet(viewsets.GenericViewSet,
                  mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin
                  ):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    lookup_field = 'username'

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


class SignUpViewSet(APIView):

    permission_classes = (permissions.AllowAny,)
    serializer = CreateUserSerializer
    queryset = User.objects.all()

    def sign_up(self, request):
        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        email = serializer.validated_data['email']
        user, confirmation_code = User.objects.get_or_create(
            username=username,
            email=email
        )
        confirmation_code = PasswordResetTokenGenerator().make_token(user)
        user.confirmation_code = confirmation_code
        user.save()
        send_mail(
            'Код подтверждения',
            f'{confirmation_code}',)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CheckConfirmationCode(APIView):

    permission_classes = (permissions.AllowAny,)
    serializer = CreateUserSerializer
    queryset = User.objects.all()

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

    http_method_names = ('get', 'post', 'patch', 'delete')
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


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет отзывов."""

    serializer_class = ReviewSerializer
    permission_classes = (IsModeratorOrAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def title_for_reviews(self):
        return get_object_or_404(
            Title,
            pk=self.kwargs.get('title_id')
        )

    def get_queryset(self):
        return self.title_for_reviews().reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.title_for_reviews()
        )


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет комментариев."""

    serializer_class = CommentSerializer
    permission_classes = (IsModeratorOrAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def commented_review(self):
        return get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'),
        )

    def get_queryset(self):
        return self.commented_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.commented_review()
        )
