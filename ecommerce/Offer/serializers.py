from rest_framework import serializers
from django.conf import settings

from Offer import models as offer_models


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = offer_models.Offer      
        depth = 1
        exclude = ('created_at', 'updated_at', 'vendor', )        