from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics


from Products import models as product_models
from Products import serializers as product_serializers


class ProductInfo(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = product_models.Product.objects.all()
    serializer_class = product_serializers.ProductSerializer
    permission_classes = [AllowAny, ]

    def retrieve(self, request, pk):
        queryset = self.get_queryset()
        try:
            instance = self.get_object()

            """
                instance.soft_delete: None of the products should be displayed if true
                if out of stock and display_out_of_stock is true then display otherwise only display if product
                is in stock.
            """
            if not settings.DISPLAY_OUT_OF_STOCK_PRODUCTS and not instance.status:
                return Response({"status": False, "data": {"msg": "Product not found."}}, status=400)

            related_products = []

            for data in instance.related_products.filter(soft_delete=False).order_by('?')[:6]:
                if data.status or not data.status and settings.DISPLAY_OUT_OF_STOCK_PRODUCTS:
                    related_products.append({
                        "id": data.id,
                        "englishName": data.english_name,
                        "nepaliName": data.nepali_name,
                        "mainImage": data.main_image.url
                    })

            product_info = {
                "englishName": instance.english_name,
                "nepaliName": instance.nepali_name,
                "oldPrice": instance.old_price,
                "price": instance.price,
                "short_description": instance.short_description,
                "description": instance.description,
                "stock": instance.status,
                "quantityLeft": instance.quantity_left,
                "delete": instance.soft_delete,
                "isFeatured": instance.is_featured,
                "brandName": instance.brand_name.name if instance.brand_name else None,
                "warranty": instance.warranty,
                "mainImage": instance.main_image.url,
                "category": [{
                    "englishName": data.english_name,
                    "nepaliName": data.nepali_name,
                    "id": data.id
                } for data in instance.category.all()],
                "sizes": [data.size for data in instance.sizes.all()],
                "relatedProducts": related_products
            }

            try:
                otherImages = []
                data = product_models.ProductImage.objects.filter(
                    product=instance)
                if data:
                    for d in data:
                        otherImages.append(d.image.url)
                product_info.update({"otherImages": otherImages})
            except (Exception, product_models.ProductImage.DoesNotExist) as e:
                print(e)
                pass
            if settings.MULTI_VENDOR:
                product_info.update(
                    {'vendor': instance.vendor.organizationName})
            return Response({"status": True, "data": product_info}, status=200)
        except (Exception) as e:
            print(e)
            return Response({"status": False, "data": {"msg": "Product not found."}}, status=400)


class CategoryInfo(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = product_models.Category.objects.all()
    serializer_class = product_serializers.CategorySerializer
    permission_classes = [AllowAny, ]

    def retrieve(self, request, pk):
        queryset = self.get_queryset()
        try:
            instance = self.get_object()
            category_info = {
                "id": instance.id,
                "englishName": instance.english_name,
                "nepaliName": instance.nepali_name,
                "image": instance.categoryImage.url
            }
            return Response({"status": True, "data": category_info}, status=200)
        except (Exception) as e:
            print(e)
            return Response({"status": False, "data": {"msg": "Category not found."}}, status=400)
