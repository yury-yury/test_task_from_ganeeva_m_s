import pytest

from tests.factories import UserFactory
from users.models import User
from users.serializers import UserSerializer


@pytest.mark.django_db
class TestUserList:
    url: str = '/users/'

    def test_users_list(self, staff_client) -> None:
        current_user = User.objects.first()
        users = UserFactory.create_batch(2)
        users.insert(0, current_user)
        response = staff_client.get(self.url)

        expected_response = {
            "count": 3,
            "next": None,
            "previous": None,
            "results": UserSerializer(users, many=True).data
        }

        assert response.status_code == 200
        assert response.json()['count'] == 3
        assert response.json()['next'] is None
        assert response.json()['previous'] is None
        assert type(response.json()['results']) == list
        assert len(response.json()['results']) == 3
        assert response.json() == expected_response

    def test_users_list_without_permission(self, auth_client) -> None:
        response = auth_client.get(self.url)


        assert response.status_code == 403
        assert response.json() == {'detail': 'You do not have permission to perform this action.'}



