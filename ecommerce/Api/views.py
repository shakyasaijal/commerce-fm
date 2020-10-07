from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets
from datetime import date
from django.db.models import Q

from Products import models as product_models
from Products import serializers as product_serializers
from Offer import models as offer_models
from Offer import serializers as offer_serializers
from User import models as user_models
from Analytics import models as analytics_model
from Api.common import api_helper
from DashboardManagement.common import emails as send_email


class FeaturedCategory(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = product_models.Category.objects.filter(
        isFeatured=True).order_by('?')[:12]
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
                "image": request.build_absolute_uri(data.categoryImage.url)
            })
        return Response({"status": True, "data": categories}, status=200)


class FeaturedProducts(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = product_models.Product.objects.filter(
        is_featured=True).order_by('?').distinct()[:12]
    serializer_class = product_serializers.FeaturedProductSerializer
    permission_classes = [AllowAny, ]

    def list(self, request):
        queryset = self.get_queryset()
        products = []
        for data in queryset:
            if data.status or not data.status and settings.DISPLAY_OUT_OF_STOCK_PRODUCTS:
                products.append({
                    "id": data.id,
                    "englishName": data.english_name,
                    "nepaliName": data.nepali_name,
                    "image": request.build_absolute_uri(data.main_image.url),
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
                "bigBannerImage": request.build_absolute_uri(data.big_banner_image.url),
                "smallBannerImage": request.build_absolute_uri(data.small_banner_image.url),
                "started": True if data.starts_from <= date.today() else False,
                "finishAfter": finish_after
            })
        return Response({"status": True, "data": offers}, status=200)

    def retrieve(self, request, pk):
        try:
            queryset = self.get_queryset().get(pk=pk)
            if (queryset.ends_at-date.today()).days < 0:
                return Response({"status": True, "data": {"msg": "Offer not available"}}, status=400)
            data = {
                "id": queryset.id,
                "title": queryset.title,
                "startsFrom": queryset.starts_from,
                "endsAt": queryset.ends_at,
                "bigBannerImage": request.build_absolute_uri(queryset.big_banner_image.url),
                "smallBannerImage": request.build_absolute_uri(queryset.small_banner_image.url),
                "started": True if queryset.starts_from <= date.today() else False,
                "finishAfter": (queryset.ends_at-date.today()).days,
                "category": [{"title": d.name, "id": d.id} for d in queryset.category.all()]
            }
            return Response({"status": True, "data": data}, status=400)
        except Exception as e:
            print(e)
            return Response({"status": True, "data": {"msg": "Offer not found"}}, status=400)


class JustForYou(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = product_models.Product.objects.all()
    serializer_class = product_serializers.ProductSerializer
    permission_classes = [AllowAny, ]

    def list(self, request):
        product_list = []
        products_in_list = []
        searched_products = []

        def product_data(products, fromSearch=False):
            if products:
                for data in products:
                    if data.id not in products_in_list:
                        product_list.append({
                            "id": data.id,
                            "englishName": data.english_name,
                            "nepaliName": data.nepali_name,
                            "mainImage": request.build_absolute_uri(data.main_image.url),
                            "oldPrice": data.old_price,
                            "price": data.price,
                            "isFeatured": data.is_featured,
                            "fromSearch": fromSearch,
                            "tags": [f.tag for f in data.tags.all()]
                        })
                        products_in_list.append(data.id)

        # From Searched Basis
        try:
            if request.user.is_authenticated:
                searched = analytics_model.SearchedKeyWord.objects.filter(
                    user=request.user).order_by('-count')[:5]
                # searched = analytics_model.SearchedAnalytics.objects.filter(
                #     user=request.user)
            else:
                searched = analytics_model.SearchedKeyWord.objects.filter(
                    user=request.new_ip.ip).order_by('-count')[:5]
                # searched = analytics_model.SearchedAnalytics.objects.get(
                #     ip=request.new_ip.ip)
        except (Exception, analytics_model.SearchedAnalytics.DoesNotExist):
            searched = None

        if searched is not None:
            # keywords = searched.keyword.all().order_by('-count')[:5]
            tags = product_models.Tags.objects.filter(
                tag__in=[d.keyword for d in searched])
            for tag in tags:
                searched_products += product_models.Product.objects.filter(
                    Q(tags__tag__iexact=tag) | Q(tags__tag__icontains=tag)).order_by('tags').distinct()

            if searched_products:
                product_data(searched_products, fromSearch=True)

        # From User interests
        if request.user.is_authenticated:
            try:
                user_profile = user_models.UserProfile.objects.get(
                    user=request.user)
            except (Exception, user_models.UserProfile.DoesNotExist):
                user_profile = None

            if user_profile is None or not user_profile.interested_category.all():
                products = product_models.Product.objects.order_by(
                    '-created_at')[:8]
            else:
                products = product_models.Product.objects.filter(
                    category__in=[d for d in user_profile.interested_category.all()]).order_by('?')[:8]

            product_data(products)

        # If not searched products and no user interests found, then  get random products
        if not product_list:
            product = product_models.Product.objects.order_by('?').all()[
                :12]
            product_data(product)

        return Response({"status": True, "data": product_list}, status=200)


class PopularOnYourArea(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = product_models.Product.objects.all()
    serializer_class = product_serializers.ProductSerializer
    permission_classes = [AllowAny, ]

    def list(self, request):
        try:
            if request.new_ip.city:
                a = user_models.IpAddress.objects.filter(
                    city=request.new_ip.city)
                # Max Sold
                # Mostly Searched
                # Wishlisted
                # In Cart
                # Mostly viewed
                print(a)
                return Response({"status": True, "data": "Under Development"}, status=200)
            else:
                return Response({"status": True, "data": "Under Development"}, status=200)
        except (Exception, user_models.IpAddress.DoesNotExist):
            return Response({"status": True, "data": "Under Development"}, status=200)


class RecentArrivals(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = product_serializers.ProductSerializer
    permission_classes = [AllowAny, ]

    def list(self, request):
        products = product_models.Product.objects.order_by(
            '-created_at')[:12]
        products_list = []
        for data in products:
            products_list.append({
                "id": data.id,
                "englishName": data.english_name,
                "nepaliName": data.nepali_name,
                "mainImage": request.build_absolute_uri(data.main_image.url),
                "oldPrice": data.old_price,
                "price": data.price
            })

        return Response({"status": True, "data": products_list}, status=200)

