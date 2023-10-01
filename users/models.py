from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    The User class is an inheritor of the AbstractUser class from the django.contrib.auth.models library.
    This is the data model contained in the user database table.
    """
    def __str__(self) -> str:
        """
        The __str__ function overrides the method of the parent class and takes no arguments except for an instance
        of its own class. When called, returns a human-readable representation of the class instance as a string.
        """
        return self.get_username()
