from rest_framework import serializers
from django.conf import settings

from User import models as user_models


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        extra_kwargs = {'password': {'write_only': True},
                        'first_name': {'required': True},
                        'last_name': {'required': True}}
        fields = ('first_name', 'last_name', 'email', 'password')
        model = user_models.User

    def create(self, validated_data):
        user = user_models.User.objects.create_user(
            **validated_data, username=validated_data['email'])
        return user


class LoginSerializer(serializers.Serializer):
    """
    Serializer for login endpoint.
    """
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)


class LogoutSerializer(serializers.Serializer):
    refreshToken = serializers.CharField(required=True)
    accessToken = serializers.CharField(required=True)


class GoogleLoginSerializer(serializers.Serializer):
    idToken = serializers.CharField(required=True)


class FacebookLoginSerializer(serializers.Serializer):
    accessToken = serializers.CharField(required=True)


class PasswordSerializer(serializers.Serializer):
    oldPassword = serializers.CharField(required=True)
    newPassword = serializers.CharField(required=True)
    confirmPassword = serializers.CharField(required=True)


class CompleteProfile(serializers.Serializer):
    phone = serializers.CharField(required=False, allow_blank=True)
    address = serializers.CharField(required=False, allow_blank=True)
    district = serializers.CharField(required=False, allow_blank=True)
    referedBy = serializers.CharField(required=False, allow_blank=True)
    interests = serializers.ListField(
        child=serializers.CharField(allow_blank=True))
