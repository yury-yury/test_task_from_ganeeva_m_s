from typing import List
from django.contrib.auth import login, logout
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import filters, status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from users.models import User
from users.permissions import IsAdminOrSelfUser
from users.serializers import UserSerializer, UserCreateSerializer, LoginSerializer


@extend_schema(summary="Users list", description="Users list with ordering, filter and pagination")
class UserListAPIView(ListAPIView):
    """
    The UserListAPIView class inherits from the parent ListAPIView class from the rest_framework.generics module.
    Represents a CBV for processing requests to the URL '/users/' using the POST method.
    """
    queryset: List[User] = User.objects.all()
    serializer_class = UserSerializer
    permission_classes: list = [IsAdminUser]
    filter_backends: list = [filters.OrderingFilter, DjangoFilterBackend,]
    ordering_fields: List[str] = ['username', 'email', 'id', 'first_name', 'last_name']
    filterset_fields: List[str] = ['username', 'email', 'id', 'first_name', 'last_name']


@extend_schema(summary="User create", description="Create a new user instance.")
class UserCreateAPIView(CreateAPIView):
    """
    The UserCreateView class inherits from the CreateAPIView class from the rest_framework.generics module and is
    a class-based view for processing requests with POST methods at the address '/core/signup'.
    """
    serializer_class = UserCreateSerializer
    permission_classes: list = [AllowAny]


@extend_schema(summary="Log User in", description="Login a new user instance.")
class LoginAPIView(CreateAPIView):
    """
    The LoginView class inherits from the CreateAPIView class from the rest_framework.generics module and is
    a class-based view for processing requests with POST methods at the address '/core/login'.
    """
    serializer_class = LoginSerializer
    permission_classes: list = [AllowAny]

    def post(self, request, *args, **kwargs) -> Response:
        """
        The post function overrides the method of the parent class. Accepts the request object and any positional
        and named arguments as parameters. If the method is called, it checks and serializes the received data
        and calls the login method for the User class object. Returns serialized object data in JSON format.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        login(request=request, user=user)
        return Response(serializer.data)


class ProfileAPIView(RetrieveUpdateDestroyAPIView):
    """
    The ProfileView class inherits from the RetrieveUpdateDestroyAPIView class from the rest_framework.generics module
    and is a class-based view for processing requests with POST, PUT, PATCH and DELETE methods at the address
     '/users/profile/{id}'.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsAdminOrSelfUser]

    @extend_schema(summary="Retrieve User.", description="Detailed view of the user profile.")
    def get(self, request, *args, **kwargs) -> User:
        """
        The get function is a method of the ProfileAPIView class that serves requests made using the GET method.
        The function overrides a base class method to enable method documentation.
        """
        return super().get(request, *args, **kwargs)

    @extend_schema(summary='Update User', description='Update profile of User')
    def put(self, request, *args, **kwargs):
        """
        The put function is a method of the ProfileAPIView class that serves requests made using the GET method.
        The function overrides a base class method to enable method documentation.
        """
        return super().put(request, *args, **kwargs)

    @extend_schema(summary='Partial update User', description='Partial update profile of User')
    def patch(self, request, *args, **kwargs):
        """
        The patch function is a method of the ProfileAPIView class that serves requests made using the GET method.
        The function overrides a base class method to enable method documentation.
        """
        return super().patch(request, *args, **kwargs)

    @extend_schema(summary="User log out.", description="Logout a user instance.")
    def delete(self, request, *args, **kwargs) -> Response:
        """
        The delete function overrides the method of the parent class. Accepts the request object and all other
        positional and named arguments as parameters. If the method is called, it calls the logout method for
        an instance of the User class corresponding to the user who made the request.
        """
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)

