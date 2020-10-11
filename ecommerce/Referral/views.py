from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.contrib.auth.models import Group
from django.db.models import Q, Sum, Count
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.conf import settings

from DashboardManagement.views import vendor_only
from DashboardManagement.common import routes as navbar
from Vendor import models as vendor_models
from Vendor import forms as vendor_forms
from User import models as user_models
from CartSystem import models as cart_models
from DashboardManagement.common import emails as send_email
from OrderAndDelivery import models as order_models
from Products import models as product_models
from Analytics import views as analytics_views
from DashboardManagement.common import helper as app_helper
from . import helper as refer_helper


template_version = "DashboardManagement/v1"
try:
    if settings.TEMPLATE_VERSION:
        template_version = "DashboardManagement/"+settings.TEMPLATE_VERSION
except Exception:
    pass


@method_decorator(vendor_only, name='dispatch')
class JoinRefer(LoginRequiredMixin, View):
    def post(self, request):
        if request.user.is_superuser:
            messages.error(request, "This feature is only for vendors.")
            return HttpResponseRedirect(reverse('vendor-home'))

        vendorUser = app_helper.current_user_vendor(request.user)
        vendorId = request.POST['vendorId']
        try:
            vendor = vendor_models.Vendor.objects.get(id=vendorId)
            if vendorUser != vendor:
                messages.warning(request, "You does not belong to this vendor")
                return HttpResponseRedirect(reverse('vendor-home'))
            refer_join = refer_helper.join_refer_by_vendor(vendor)
            if refer_join[0]:
                messages.success(request, refer_join[1])
            else:
                messages.error(request, refer_join[1])
            return HttpResponseRedirect(reverse('vendor-home'))
        except (Exception, vendor_models.Vendor.DoesNotExist) as e:
            print(e, "<<<<<<<<<<<<<<<<<<")
            messages.error(request, "Vendor does not exists.")
            return HttpResponseRedirect(reverse('vendor-home'))
