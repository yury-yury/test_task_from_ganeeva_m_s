import os
import sys

import rest_framework
import django

# import task_from_ganeeva

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "task_from_ganeeva.settings")
# django.setup()
# task_from_ganeeva.settings.configure()

# from django.conf import settings
#
# from task_from_ganeeva.settings import BASE_DIR
#
# settings.configure()
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
# sys.path.append(BASE_DIR)

import pytest
from rest_framework.test import APIClient

from users.models import User


pytest_plugins = 'tests.factories'


@pytest.fixture
def client() -> APIClient:
    """
    The client function is a pytest fixture and overrides the Django test client. Does not accept parameters.
    Returns a test client from the rest_framework.test library.
    """
    return APIClient()


@pytest.fixture
def auth_client(client, user: User) -> APIClient:
    """
    The auth_client API Client function is a pytest fixture and overrides the test client. Accepts a test client
    and an instance of the User class as parameters. Performs user authentication. Returns a test client
    with authentication performed from the rest_framework.test library.
    """
    client.force_login(user)
    return client


@pytest.fixture
def staff_client(client, user: User) -> APIClient:
    setattr(user, "is_staff", True)
    setattr(user, "is_superuser", True)
    user.save()
    client.force_login(user)
    return client

