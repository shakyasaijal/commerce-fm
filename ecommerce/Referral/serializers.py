from rest_framework import serializers
from django.conf import settings

from Referral import models as refer_models


class JoinSerializer(serializers.Serializer):
    accessToken = serializers.CharField(required=True)

