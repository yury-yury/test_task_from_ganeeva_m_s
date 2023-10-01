import pytest

from users.models import User


class TestUserModel:
    """
    The TestUserModel class is a test class designed to test the functionality of a data model.
    Contains unit tests for testing using the Pytest library.
    """

    def test_create_user(self) -> None:
        """
        The test_create_user function is designed to test the correct operation
        of the User data model when creating a new instance.
        """
        user = User(username='pytest')
        assert user.username == 'pytest'
        assert str(user) == "pytest"
        assert user.is_superuser == False
        assert user.first_name == ''
        assert user.last_name == ''


    @pytest.mark.django_db
    def test_create_user_superuser(self, user: User) -> None:
        """
        The test_create_user function is designed to check the correct operation
        of the User data model when creating a new instance that is a superuser.
        """
        setattr(user, 'is_superuser', True)
        assert user.is_superuser
