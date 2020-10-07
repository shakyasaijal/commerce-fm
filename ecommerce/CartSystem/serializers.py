from rest_framework import serializers
from django.conf import settings

from CartSystem import models as cart_models
from User import models as user_models
from User import serializers as user_serializers
from Products import models as product_models


class WishlistProduct(serializers.ModelSerializer):
    class Meta:
        model = product_models.Product
        fields = ['id', 'english_name', 'nepali_name',
                  'old_price', 'price', 'main_image']


class WishlistSerializer(serializers.ModelSerializer):
    product = WishlistProduct()

    class Meta:
        fields = ['product']
        model = cart_models.WishList
        depth = 2


class AddToCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = cart_models.AddToCart
        fields = '__all__'
