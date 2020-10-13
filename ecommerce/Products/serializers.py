from rest_framework import serializers
from django.conf import settings

from Products import models as product_models
from Vendor import models as vendor_models


class FeaturedCategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = product_models.Category


class FeaturedProductSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = product_models.Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = product_models.Product
        depth = 1
        exclude = ('tags', 'created_at', 'updated_at', 'soft_delete')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = product_models.Category


class CommentSerializer(serializers.Serializer):
    comment = serializers.CharField(required=False)
    productId = serializers.CharField(required=False)
    commentId = serializers.CharField(required=False, allow_blank=True)
