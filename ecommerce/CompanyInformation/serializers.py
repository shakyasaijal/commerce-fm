from rest_framework import serializers
from django.conf import settings

from CompanyInformation import models as company_models


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = company_models.CompanyInformation
        fields = '__all__'
        depth = 2


class SocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = company_models.SocialMedia
        exclude = ['id']