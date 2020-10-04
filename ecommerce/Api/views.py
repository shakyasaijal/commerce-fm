from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets
from datetime import date

from Products import models as product_models
from Products import serializers as product_serializers
from Offer import models as offer_models
from Offer import serializers as offer_serializers


def SystemInfo(request):
    multiVendor = settings.MULTI_VENDOR
    addToCartWithoutLogin = settings.ADD_TO_CART_WITHOUT_LOGIN
    hasAdditionalData = settings.HAS_ADDITIONAL_USER_DATA
    mustHaveAdditionalData = settings.MUST_HAVE_ADDITIONAL_DATA

    return JsonResponse({"multiVendor": multiVendor, "addToCartWithoutLogin": addToCartWithoutLogin, "hasAdditionalData": hasAdditionalData, "mustHaveAdditionalData": mustHaveAdditionalData})


class FeaturedCategory(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = product_models.Category.objects.filter(isFeatured=True).order_by('?')[:12]
    serializer_class = product_serializers.FeaturedCategorySerializer
    permission_classes = [AllowAny, ]

    def list(self, request):
        queryset = self.get_queryset()
        categories = []
        for data in queryset:
            categories.append({
                "id": data.id,
                "englishName": data.english_name,
                "nepaliName": data.nepali_name,
                "image": data.categoryImage.url
            })
        return Response({"status": True, "data": categories}, status=200)


class FeaturedProducts(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = product_models.Product.objects.filter(is_featured=True).order_by('?').distinct()[:12]
    serializer_class = product_serializers.FeaturedProductSerializer
    permission_classes = [AllowAny, ]

    def list(self, request):
        queryset = self.get_queryset()
        products = []
        for data in queryset:
            products.append({
                "id": data.id,
                "englishName": data.english_name,
                "nepaliName": data.nepali_name,
                "image": data.main_image.url,
                "oldPrice": data.old_price,
                "newPrice": data.price
            })
        return Response({"status": True, "data": products}, status=200)



class Offers(mixins.ListModelMixin, viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    queryset = offer_models.Offer.objects.all()
    serializer_class = offer_serializers.OfferSerializer
    permission_classes = [AllowAny, ]

    def list(self, request):
        queryset = self.get_queryset().filter(ends_at__gte=date.today())
        if not queryset:
            return Response({"status": False, "data": []}, status=200)
        offers = []
        for data in queryset:
            finish_after = (data.ends_at-date.today()).days
            offers.append({
                "id": data.id,
                "title": data.title,
                "startsFrom": data.starts_from,
                "endsAt": data.ends_at,
                "bigBannerImage": data.big_banner_image.url,
                "smallBannerImage": data.small_banner_image.url,
                "started": True if data.starts_from <= date.today() else False,
                "finishAfter": finish_after
            })
        return Response({"status": True, "data": offers}, status=200)

    def retrieve(self, request, pk):
        try:
            queryset = self.get_queryset().get(pk=pk)
            if (queryset.ends_at-date.today()).days < 0:
                return Response({"status": True, "data": {"msg": "Offer not available"}}, status=400)
            print(request.ip)
            data = {
                "id": queryset.id,
                "title": queryset.title,
                "startsFrom": queryset.starts_from,
                "endsAt": queryset.ends_at,
                "bigBannerImage": queryset.big_banner_image.url,
                "smallBannerImage": queryset.small_banner_image.url,
                "started": True if queryset.starts_from <= date.today() else False,
                "finishAfter": (queryset.ends_at-date.today()).days,
                "category": [{"title": d.name, "id": d.id} for d in queryset.category.all()]
            }
            return Response({"status": True, "data": data}, status=400)
        except Exception as e:
            print(e)
            return Response({"status": True, "data": {"msg": "Offer not found"}}, status=400)
