from django.shortcuts import render, redirect, reverse
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.utils.decorators import method_decorator
from functools import wraps
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q

from DeliverySystem import models as delivery_models
from OrderAndDelivery import models as order_models
from . import utils as delivery_utils


# Create your views here.
template_version = "DeliverySystem/v1"
try:
    if settings.TEMPLATE_VERSION:
        template_version = "DeliverySystem/"+settings.TEMPLATE_VERSION
except Exception:
    pass


def deliveryPerson_only(function):
    @wraps(function)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Please login.')
            return HttpResponseRedirect(reverse('delivery-login'))
        if request.user.is_superuser:
            return function(request, *args, **kwargs)
        else:
            try:
                if delivery_models.DeliveryPerson.objects.get(user=request.user):
                    return function(request, *args, **kwargs)
            except (Exception, delivery_models.DeliveryPerson.DoesNotExist) as e:
                print(e, ">>")
                messages.warning(request, 'Access to delivery person only.')
                return render(request, template_version+"/Views/LoginView/login.html")
        return function(request, *args, **kwargs)
    return _wrapped_view


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('delivery-index'))
        return render(request, template_version+"/Views/LoginView/login.html")

    def post(self, request):

        user = authenticate(
            request, username=request.POST['email'], password=request.POST['password'])

        if user is not None:
            try:
                delivery_person = delivery_models.DeliveryPerson.objects.get(
                    user=user)
                login(request, user)
                return HttpResponseRedirect(reverse('delivery-index'))
            except (Exception, delivery_models.DeliveryPerson.DoesNotExist):
                return redirect(settings.FRONTEND_URL)
        else:
            messages.warning(request, 'Invalid email/password.')
            return HttpResponseRedirect(reverse('delivery-login'))


@method_decorator(deliveryPerson_only, name='dispatch')
class Index(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, template_version+"/Views/index.html")


@method_decorator(deliveryPerson_only, name='dispatch')
class OrderView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_superuser:
            orders = order_models.Order.objects.filter(
                ~Q(status=3)).order_by('created_at', 'status')
        else:
            all_orders = order_models.Order.objects.filter(
                Q(district__in=delivery_utils.get_my_delivery_district(request.user)) & ~Q(status=3)).order_by('created_at', 'status')
            my_delivery_object = delivery_utils.get_my_delivery_object(
                request.user)
            orders = []
            for data in all_orders:
                if not data.direct_assign or data.direct_assign == my_delivery_object:
                    orders.append(data)
        return render(request, template_version+"/Views/Orders/list.html", context={"orders": orders})


@method_decorator(deliveryPerson_only, name='dispatch')
class OrderDetail(LoginRequiredMixin, View):
    def get(self, request, id):
        try:
            order = order_models.Order.objects.get(id=id)
        except (Exception, order_models.Order.DoesNotExist):
            messages.error(request, "No order found.")
            return HttpResponseRedirect(reverse('delivery-order'))

        my_delivery_object = delivery_utils.get_my_delivery_object(
            request.user)

        flag = False

        if order.direct_assign:
            if order.direct_assign != my_delivery_object:
                messages.warning(
                    request, "You are not allowed to view this order.")
                return HttpResponseRedirect(reverse('delivery-order'))
            else:
                flag = True

        if order.district not in my_delivery_object.based_on_district.all():
            messages.warning(
                request, "You are not allowed to view this order.")
            return HttpResponseRedirect(reverse('delivery-order'))
        else:
            flag = True

        if flag:
            return render(request, template_version+"/Views/Orders/detail.html", context={"order": order})
        else:
            return HttpResponseRedirect(reverse('delivery-order'))
