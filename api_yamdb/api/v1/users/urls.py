from django.urls import include, path
from rest_framework import routers

from api.v1.users import views

router_users_v1 = routers.DefaultRouter()

router_users_v1.register('users', views.UserViewSet, basename='users')

urlpatterns = [
    path('', include(router_users_v1.urls)),
    path('auth/signup/', views.sign_up),
    path('auth/token/', views.check_code, name='check_code'),
]
