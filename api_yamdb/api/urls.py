from django.urls import include, path
from rest_framework import routers

from api import views

router_v1 = routers.DefaultRouter()

router_v1.register('users', views.UserViewSet, basename='users')
router_v1.register('titles', views.TitleViewSet, basename='titles')
router_v1.register('genres', views.GenreViewSet, basename='genres')
router_v1.register('categories', views.CategoryViewSet, basename='category')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    views.ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', views.sign_up),
    path('v1/auth/token/', views.CheckToken, name='check_code'),
]
