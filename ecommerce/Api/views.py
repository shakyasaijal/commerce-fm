from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse


def SystemInfo(request):
    multiVendor = settings.MULTI_VENDOR
    addToCartWithoutLogin = settings.ADD_TO_CART_WITHOUT_LOGIN
    hasAdditionalData = settings.HAS_ADDITIONAL_USER_DATA
    mustHaveAdditionalData = settings.MUST_HAVE_ADDITIONAL_DATA

    return JsonResponse({"multiVendor": multiVendor, "addToCartWithoutLogin": addToCartWithoutLogin, "hasAdditionalData": hasAdditionalData, "mustHaveAdditionalData": mustHaveAdditionalData})