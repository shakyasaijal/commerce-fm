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
        user = user_models.User.objects.create_user(**validated_data, username=validated_data['email'])
        return user


class UserSeriaizer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = user_models.User
