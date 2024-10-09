from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from rest_framework import serializers

from .models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_password(self, password: str):
        try:
            validate_password(password)
            return password

        except exceptions.ValidationError as e:
            raise serializers.ValidationError(e.messages)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "is_staff"]
