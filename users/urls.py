from django.urls import path

from users.views import (
    UserCreateAPIView,
    LoginAPIView,
    ProfileAPIView, UserListAPIView)


urlpatterns = [
    path('signup', UserCreateAPIView.as_view()),
    path('login', LoginAPIView.as_view()),
    path('profile/<int:pk>', ProfileAPIView.as_view()),
    path('', UserListAPIView.as_view())
]
