import pytest

from users.models import User


@pytest.mark.django_db
def test_user_create():
    user = User.objects.create(username='test')
    assert user.username == 'test'
    assert str(user) == 'test'
    assert isinstance(user, User)
