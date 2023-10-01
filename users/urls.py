from django.urls import path, include
from rest_framework import routers

from users.views import (
    UserCreateAPIView,
    LoginAPIView,
    ProfileAPIView, UserListAPIView)

# from users_test.views import UserViewSet

# router = routers.SimpleRouter()
# router.register('', UserViewSet, basename='user')

# urlpatterns = [
#     path('create/', UserCreateAPIView.as_view()),
#     path('list/', UserListAPIView.as_view()),
#     path('<int:pk>', UserAPIView.as_view()),
# ]
urlpatterns = [
    # path('drf/', include('rest_framework.urls')),
    path('signup', UserCreateAPIView.as_view()),
    path('login', LoginAPIView.as_view()),
    path('profile/<int:pk>', ProfileAPIView.as_view()),
    path('', UserListAPIView.as_view())
]
