from typing import List
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from users.models import User


class UserCreateSerializer(serializers.ModelSerializer):
    """
    The UserCreateSerializer class inherits from the ModelSerializer class from rest_framework.serializers.
    This is a class for convenient serialization and deserialization of objects of the User class when processing
    create new instance of User class.
    """
    id = serializers.IntegerField(required=False, read_only=True)
    password = serializers.CharField(write_only=True)
    password_repeat = serializers.CharField(write_only=True)

    class Meta:
        """
        The Meta class is an internal service class of the serializer,
        defines the necessary parameters for the serializer to function.
        """
        model = User
        fields: List[str] = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'password_repeat']

    def validate(self, attrs) -> dict:
        """
        The validate function overrides the method of the parent class. Takes the values of the class instance
        attributes as parameters. Calls the parent method and adds password complexity checks in accordance with
        the specified validators and the coincidence of the received values 'password' and 'password_repeat',
        raises a ValidationError exception if there are differences. After comparison, deletes the key and the value
        of 'password_repeat'. Returns the date object.
        """
        data: dict = super().validate(attrs)
        validate_password(data['password'])
        if data['password'] != data['password_repeat']:
            raise serializers.ValidationError('The entered passwords must match')
        del data['password_repeat']
        return data

    def create(self, validated_data) -> User:
        """
        The create function overrides the method of the parent class. Takes validated_data values as parameters.
        Creates an instance of the User class, adds the value of the hashed password, and stores the object
        in the database. Returns the created object.
        """
        user: User = User(
            username=validated_data['username'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            email=validated_data.get('email', ''),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginSerializer(serializers.ModelSerializer):
    """
    The LoginSerializer class inherits from the ModelSerializer class from rest_framework.serializers.
    This is a class for convenient serialization and deserialization of objects of the User class when processing
    login instance of User class.
    """
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    class Meta:
        """
        The Meta class is an internal service class of the serializer,
        defines the necessary parameters for the serializer to function.
        """
        model = User
        fields: List[str] = ['id', 'username', 'first_name', 'last_name', 'email', 'password']

    def create(self, validated_data) -> User:
        """
        The create function overrides the method of the parent class. Takes validated_data values as parameters.
        Authenticates an instance of the User class according to the values received, raises an AuthenticationFailed
        exception if there is no user information or incorrect data in the database. Returns the found object.
        """
        user = authenticate(username=validated_data['username'], password=validated_data['password'])
        if user is None:
            raise AuthenticationFailed
        return user


class UserSerializer(serializers.ModelSerializer):
    """
    The UserSerializer class inherits from the ModelSerializer class from rest_framework.serializers.
    This is a class for convenient serialization and deserialization of objects of the User class.
    """
    class Meta:
        """
        The Meta class is an internal service class of the serializer,
        defines the necessary parameters for the serializer to function.
        """
        model = User
        fields: List[str] = ['id', 'username', 'first_name', 'last_name', 'email']

