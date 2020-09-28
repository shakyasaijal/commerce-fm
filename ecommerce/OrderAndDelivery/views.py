from django.shortcuts import render, redirect, reverse
from django.conf import settings
from django.utils.decorators import method_decorator
from functools import wraps
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.forms import modelformset_factory, inlineformset_factory
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.db.models import Q

from Vendor import models as vendor_models
from CartSystem import models as cart_models
from Products import models as product_models
from OrderAndDelivery import models as order_models
from User import models as user_models
from DashboardManagement.common import routes as navbar
from DashboardManagement.common import helper as app_helper
from DashboardManagement.validator import create as create_validation
from DashboardManagement.common import create as create_helper
from Products import forms as product_forms
from DashboardManagement.common import validation as validations
from DashboardManagement.views import vendor_only


template_version = "DashboardManagement/v1"
try:
    if settings.TEMPLATE_VERSION:
        template_version = "DashboardManagement/"+settings.TEMPLATE_VERSION
except Exception:
    pass


@method_decorator(vendor_only, name='dispatch')
class OrderView(LoginRequiredMixin, View):
    def get(self, request):
        if not app_helper.access_management('OrderAbdDelivery.view_order', request):
            messages.error(request, "You don't have permission to view orders")
            return HttpResponseRedirect(reverse('vendor-home'))

        if settings.MULTI_VENDOR:
            orders = order_models.Order.objects.filter(
                Q(vendor=app_helper.current_user_vendor(request.user)) and ~Q(status=3))
        else:
            orders = order_models.Order.objects.all().filter(~Q(status=3))

        routes = navbar.get_formatted_routes(navbar.get_routes(
            request.user), active_page='orders')
        
        # order_page = True is for removing container-fluid from base.html and navbar padding
        context = {
            "routes": routes,
            "orders": orders,
            "title": "Order",
            "sub_navbar": "pending/new orders",
            "order_page": True
        }
        return render(request, template_version+"/Views/Products/order/order.html", context=context)


@method_decorator(vendor_only, name='dispatch')
class DeliveredView(LoginRequiredMixin, View):
    def get(self, request):
        if not app_helper.access_management('OrderAbdDelivery.view_order', request):
            messages.error(request, "You don't have permission to view orders")
            return HttpResponseRedirect(reverse('vendor-home'))

        if settings.MULTI_VENDOR:
            orders = order_models.Order.delivered_objects.filter(
                vendor=app_helper.current_user_vendor(request.user))
        else:
            orders = order_models.Order.delivered_objects.all()

        routes = navbar.get_formatted_routes(navbar.get_routes(
            request.user), active_page='orders')

        # order_page = True is for removing container-fluid from base.html and navbar padding
        context = {
            "routes": routes,
            "orders": orders,
            "title": "Orders Delivered",
            "sub_navbar": "delivered orders",
            "order_page": True
        }
        return render(request, template_version+"/Views/Products/order/delivered.html", context=context)
