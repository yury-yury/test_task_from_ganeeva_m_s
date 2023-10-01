from django.contrib.auth import login, logout
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response

from users.models import User
from users.permissions import IsAdminOrSelfUser
from users.serializers import UserSerializer, UserCreateSerializer, LoginSerializer


class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [filters.OrderingFilter,
                       DjangoFilterBackend,]
    ordering_fields = ['username', 'email', 'id', 'first_name', 'last_name']
    filterset_fields = ['username', 'email', 'id', 'first_name', 'last_name']


# class UserCreateAPIView(CreateAPIView):
#     model = User
#     serializer_class = UserCreateSerializer
#
#
# class UsersAPIView(ListCreateAPIView):
#     model = User
#     queryset = User.objects.all()
#
#     def get_serializer_class(self):
#         pass
#
#
# class UserAPIView(RetrieveUpdateDestroyAPIView):
#     model = User
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


class UserCreateAPIView(CreateAPIView):
    """
    The UserCreateView class inherits from the CreateAPIView class from the rest_framework.generics module and is
    a class-based view for processing requests with POST methods at the address '/core/signup'.
    """
    model = User
    serializer_class = UserCreateSerializer
    permission_classes: list = [AllowAny]


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
     '/core/profile'.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdminOrSelfUser]

    # def get_object(self) -> User:
    #     """
    #     The get_object function overrides the method of the parent class. It does not accept arguments as parameters,
    #     except for the instance itself. If the method is called, it returns an instance of the User class corresponding
    #     to the user who made the request.
    #     """
    #     return self.request.user

    def delete(self, request, *args, **kwargs) -> Response:
        """
        The delete function overrides the method of the parent class. Accepts the request object and all other
        positional and named arguments as parameters. If the method is called, it calls the logout method for
        an instance of the User class corresponding to the user who made the request.
        """
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)

