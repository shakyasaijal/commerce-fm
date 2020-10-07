from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics


from Products import models as product_models
from Products import serializers as product_serializers
from CartSystem.common import cart_system as cart_helper
from CartSystem import serializers as cart_serializers
from CartSystem import models as cart_models


class Wishlist(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = cart_models.WishList.objects.all()
    serializer_class = cart_serializers.WishlistSerializer
    permission_classes = [IsAuthenticated, ]

    def list(self, request):
        wishlist = cart_helper.get_wishlist_by_user(request)
        return Response({"status": True, "data": wishlist}, status=200)


class CartItems(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = cart_models.AddToCart.objects.none()
    serializer = cart_serializers.AddToCartSerializer
    permission_classes = [AllowAny, ]

    def list(self, request):
        cart = cart_helper.get_user_cart(request)
        return Response({"status": True, "data": {"cartItem": cart[0], "grandTotal": cart[1]}}, status=200)


class WishlistToCart(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = cart_models.WishList.objects.none()
    serializer = cart_serializers.WishlistProduct
    permission_classes = [IsAuthenticated, ]

    def create(self, request):
        if not request.data["quantity"] or request.data["wishlistId"]:
            return Response({"status": False, "data": {"msg": "Data is missing. Please try again."}}, status=400)

        try:
            wishlist = cart_models.WishList.objects.get(
                id=request.data["wishlistId"])
            new_cart = cart_models.AddToCart.objects.get_or_create(
                user=request.user, product=wishlist.product, quantity=request.data["quantity"])
            if new_cart:
                if not wishlist.delete():
                    new_cart.delete()
                    return Response({"status": False, "data": {"msg": "Something went wrong. Please try again."}}, status=400)
            else:
                return Response({"status": False, "data": {"msg": "Something went wrong. Please try again."}}, status=400)
            return Response({"status": True, "data": {"msg": "Successfully added to cart."}}, status=200)
        except (Exception, cart_models.WishList.DoesNotExist):
            return Response({"status": False, "data": {"msg": "Data not found."}}, status=400)
