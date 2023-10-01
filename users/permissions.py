from rest_framework.permissions import BasePermission


class IsAdminOrSelfUser(BasePermission):
    """
    Allows access only to authenticated users_test.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        elif request.user.id == obj.id:
            return True
        return False
