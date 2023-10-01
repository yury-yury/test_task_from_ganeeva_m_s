import factory.django
from django.db import models
from django.utils import timezone
from pytest_factoryboy import register

from users.models import User


@register
class UserFactory(factory.django.DjangoModelFactory):
    """
    The UserFactory class inherits from the parent class DjangoModelFactory from the factory.django module.
    It is intended for creating instances of the User class in order to conduct unit tests of the functioning
    of applications using the pytest library.
    """
    username = factory.Faker('user_name')
    password = factory.Faker('password')

    class Meta:
        """
        The Meta class is an internal utility class. Contains the name of the model for the purpose
        of creating test instances.
        """
        model: models.Model = User

    @classmethod
    def _create(cls, model_class, *args, **kwargs) -> User:
        """
        The _create function overrides the protected class method of the parent class. Accepts the model_class
        object and all other positional and named arguments as parameters. Creates and returns an instance
        of the User class.
        """
        return User.objects.create(*args, **kwargs)
