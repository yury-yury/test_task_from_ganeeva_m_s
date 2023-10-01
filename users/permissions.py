from rest_framework.permissions import BasePermission

from users.models import User


class IsAdminOrSelfUser(BasePermission):
    """
    The IsAdminOrSelfUser class inherits from the BasePermission class from the permissions module
    of the rest_framework library. Controls access to protected endpoints.
    """
    def has_object_permission(self, request, view, obj: User) -> bool:
        """
        The has_object_permission function is a method of the IsAdminOrSelfUser class.
        Takes request, view, and an instance of the User class as arguments.
        Upon request, checks whether the user who made the request is the profile owner or has superuser status.
        If the result is positive, returns True; otherwise, False.
        """
        if request.user.is_superuser:
            return True
        elif request.user.id == obj.pk:
            return True
        return False
