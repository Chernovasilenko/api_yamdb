from django.urls import include, path
from rest_framework import routers

from . import views

router_reviews_v1 = routers.DefaultRouter()

router_reviews_v1.register('titles', views.TitleViewSet, basename='titles')
router_reviews_v1.register('genres', views.GenreViewSet, basename='genres')
router_reviews_v1.register(
    'categories',
    views.CategoryViewSet,
    basename='category'
)
router_reviews_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    views.ReviewViewSet,
    basename='reviews'
)
router_reviews_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('', include(router_reviews_v1.urls)),
]
