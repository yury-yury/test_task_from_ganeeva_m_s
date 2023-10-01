import pytest

from tests.factories import UserFactory
from users.models import User
from users.serializers import UserSerializer


@pytest.mark.django_db
class TestUserProfile:
    url = '/users/profile/'

    def test_get_user_profile_for_self(self, auth_client):
        current_user = User.objects.first()

        response = auth_client.get(self.url + f'{current_user.id}')

        assert response.status_code == 200
        assert response.json() == UserSerializer(current_user).data


    def test_get_user_profile_for_superuser(self, staff_client):
        current_user = User.objects.first()
        user = UserFactory.create()

        response = staff_client.get(self.url + f'{current_user.id + 1}')

        assert response.status_code == 200
        assert response.json() == UserSerializer(user).data

    def test_get_user_profile_without_permission(self, auth_client):
        current_user = User.objects.first()
        user = UserFactory.create()

        response = auth_client.get(self.url + f'{current_user.id + 1}')

        assert response.status_code == 403

    def test_patch_user_profile_for_self(self, auth_client):
        current_user = User.objects.first()

        response = auth_client.patch(self.url + f'{current_user.id}', params={
            "first_name": "test", "last_name": "test"
        })

        user = User.objects.first()

        assert response.status_code == 200
        assert response.json() == UserSerializer(user).data

    def test_delete_user_profile_for_admin(self, staff_client):
        current_user = UserFactory.create()

        response = staff_client.delete(self.url + f'{current_user.id}')

        assert response.status_code == 204
