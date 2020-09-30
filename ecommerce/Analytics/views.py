from django.shortcuts import render
from django.conf import settings
from django.db.models import Count
from django.db.models import Q
from datetime import date, timedelta


from Analytics import models as analytics_model
from Vendor import models as vendor_models
from Products import models as product_models
from CartSystem import models as cart_models
from User import models as user_models
from OrderAndDelivery import models as order_models
from DashboardManagement.common import helper


def highly_searched_keyword():
    data = analytics_model.SearchedKeyWord.objects.all().order_by(
        -count)[:10]
    return data


if settings.MULTI_VENDOR:
    def max_vendor_user():
        data = vendor_models.Vendor.objects.values('organizationName').annotate(
            total=Count('vendorUsers')).order_by('-total')[:5]
        return data


def popular_brand():
    brand = product_models.Product.objects.values('brand_name__name').annotate(
        total=Count('brand_name')).order_by('brand_name')[:10]
    return brand


def popular_product__wishlist():
    wishlist = cart_models.WishList.objects.values('product__english_name').annotate(
        total=Count('product')).order_by('product')[:10]
    return wishlist


def popular_location():
    location = user_models.UserProfile.objects.all().values('district__province', 'district__district').annotate(
        total=Count('district')).order_by('district').filter(~Q(district=None))


def new_orders(user):
    if settings.MULTI_VENDOR and not user.is_superuser:
        orders = order_models.Order.objects.filter(
            ~Q(status=3) and Q(vendor=helper.current_user_vendor(user))).count()
    else:
        orders = order_models.Order.objects.filter(~Q(status=3)).count()

    return orders


def users(user):
    if settings.MULTI_VENDOR and not user.is_superuser:
        vendor = helper.current_user_vendor(user)
        vendor_user = vendor.vendorUsers.count()
    else:
        vendor_user = user_models.User.objects.filter(is_superuser=True).count()

    return vendor_user


def new_customer_registered_in_week():
    d=date.today()-timedelta(days=7)
    users = user_models.User.objects.filter(date_joined__gte=d).count()
    return users


def total_products(user):
    if settings.MULTI_VENDOR and not user.is_superuser:
        products = product_models.Product.objects.filter(vendor=helper.current_user_vendor(user)).count()
    else:
        products = product_models.Product.objects.all().count()

    return products