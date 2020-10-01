from django.shortcuts import render
from django.conf import settings
from datetime import date, timedelta
from django.db.models import Q, Count, Sum
from collections import Counter 


from Analytics import models as analytics_model
from Vendor import models as vendor_models
from Products import models as product_models
from CartSystem import models as cart_models
from User import models as user_models
from OrderAndDelivery import models as order_models
from DashboardManagement.common import helper


def highly_searched_keyword():
    data = analytics_model.SearchedKeyWord.objects.all().order_by('-count')[:20]
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


def top_five_category(vendor):
    # Top 5 buyed category and highest & lowest sold product Start
    highest_ordered = order_models.Order.delivered_objects.filter(vendor=vendor)
    highest_ordered_category = {}
    for data in highest_ordered:
        for d in data.item.all():
            if d.item.vendor == vendor:
                for category in d.item.category.all()[:1]:
                    if category.english_name in highest_ordered_category:
                        highest_ordered_category[category.english_name] = d.quantity + highest_ordered_category[category.english_name]
                    else:
                        highest_ordered_category[category.english_name] = d.quantity
    top_five = sorted(highest_ordered_category.items(), key=lambda x: x[1], reverse=True)
    identify = Counter(top_five)
    highest = identify.most_common(5)
    highest_ordered_category = {}
    for data in highest:
        highest_ordered_category.update({data[0][0]:data[0][1]}) #include
 
    return highest_ordered_category


def highest_and_lowest_sold(vendor):
    '''
        Maximum sold product and
        Minimum sold product
    '''
    highest_ordered = order_models.Order.delivered_objects.filter(vendor=vendor)
    highest_ordered_category = {}
    highest_ordered_product = {}
    for data in highest_ordered:
        for d in data.item.all():
            if d.item.vendor == vendor:
                if d.item.english_name in highest_ordered_product:
                    highest_ordered_product[d.item.english_name] = d.quantity + highest_ordered_product[d.item.english_name]
                else:
                    highest_ordered_product[d.item.english_name] = d.quantity
    response = {}
    for data in sorted(highest_ordered_product, key=highest_ordered_product.get, reverse=True)[:1]:
        response[data] = highest_ordered_product[data] #include

    for data in sorted(highest_ordered_product, key=highest_ordered_product.get)[:1]:
        response[data] = highest_ordered_product[data] #include

    return response
