import pytest

from users.models import User


def test_create_user():
    user = User(username='pytest')
    assert user.username == 'pytest'
    assert str(user) == "pytest"
    assert user.is_superuser == False
    assert user.first_name == ''
    assert user.last_name == ''


@pytest.mark.django_db
def test_create_user_superuser(user):
    setattr(user, 'is_superuser', True)
    assert user.is_superuser
