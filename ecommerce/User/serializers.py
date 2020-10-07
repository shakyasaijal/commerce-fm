from rest_framework import serializers
from django.conf import settings

from User import models as user_models


class UserSerializer(serializers.ModelSerializer):
        fields = '__all__'
        model = user_models.User