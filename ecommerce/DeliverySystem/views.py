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
import datetime

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
        data = delivery_utils.index_data(request.user)
        context = {}
        context.update(data)

        return render(request, template_version+"/Views/index.html")


@method_decorator(deliveryPerson_only, name='dispatch')
class OrderView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_superuser:
            all_orders = order_models.Order.objects.filter(
                ~Q(status=3)).order_by('created_at', 'status')
        else:
            my_delivery_object = delivery_utils.get_my_delivery_object(
                request.user)
            all_orders = delivery_utils.total_pending_orders(request.user)
            my_delivery_object = delivery_utils.get_my_delivery_object(
                request.user)
        return render(request, template_version+"/Views/Orders/list.html", context={"orders": all_orders})


@method_decorator(deliveryPerson_only, name='dispatch')
class OrderDetail(LoginRequiredMixin, View):
    def get(self, request, id):
        print(delivery_utils.orders_to_be_taken(request.user))
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
        else:
            if order.district not in my_delivery_object.based_on_district.all():
                messages.warning(
                    request, "You are not allowed to view this order.")
                return HttpResponseRedirect(reverse('delivery-order'))
            else:
                flag = True

        if flag:
            order_items = []
            sub_total = 0

            delivery_charge = 0

            for data in order.item.all():
                sub_price = data.quantity * data.item.price
                sub_total += sub_price
                orderData = {
                    "en_name": data.item.english_name,
                    "np_name": data.item.nepali_name,
                    "quantity": data.quantity,
                    "price": data.item.price,
                    "sub_product_total": sub_price
                }
                if settings.MULTI_VENDOR:
                    orderData.update({"vendor": data.item.vendor})
                order_items.append(orderData)
            total_price = delivery_charge + sub_total
            total_bill = {
                "sub_total": sub_total,
                "delivery_charge": 0,
                "total_price": total_price
            }
            context = {}
            context.update({"order": order})
            context.update({"order_items": order_items})
            context.update({"total_bill": total_bill})
            context.update({"my_delivery_object": my_delivery_object})
            return render(request, template_version+"/Views/Orders/detail.html", context=context)
        else:
            return HttpResponseRedirect(reverse('delivery-order'))


@method_decorator(deliveryPerson_only, name='dispatch')
class MyDelivery(LoginRequiredMixin, View):
    def get(self, request):
        my_delivery_obj = delivery_utils.get_my_delivery_object(request.user)
        orders = order_models.Order.objects.filter(Q(direct_assign=my_delivery_obj) | Q(delivery_by=my_delivery_obj) & ~Q(status=3) & ~Q(status=4)).order_by('created_at')
        context = {}
        context.update({"orders": orders})
        context.update({"title": "My Delivery"})
        return render(request, template_version+"/Views/Orders/myDelivery.html", context=context)


@method_decorator(deliveryPerson_only, name='dispatch')
class PendingDelivery(LoginRequiredMixin, View):
    def get(self, request):
        orders = order_models.Order.objects.filter(~Q(status=3) & ~Q(status=4) & Q(direct_assign__isnull=True) & Q(delivery_by__isnull=True)).order_by('created_at')
        context = {}
        context.update({"orders": orders})
        context.update({"title": "All Pending To Take Delivery."})
        return render(request, template_version+"/Views/Orders/pending.html", context=context)


@method_decorator(deliveryPerson_only, name='dispatch')
class TakeDelivery(LoginRequiredMixin, View):
    def post(self, request):

        # Have order with this id.
        try:
            order = order_models.Order.objects.get(id=request.POST['orderId'])
        except (Exception, order_models.Order.DoesNotExist):
            messages.error(request, "No order found.")
            return HttpResponseRedirect(reverse('delivery-order'))

        # Have direct assign.
        # No need to take delivery if it has been assigned.
        if order.direct_assign:
            messages.warning(request, "This order is deliverying by {}".format(
                order.direct_assign.user.get_full_name()))
            return HttpResponseRedirect(reverse('delivery-order'))
        else:
            # Belongs to my delivery location
            my_delivery_object = delivery_utils.get_my_delivery_object(
                request.user)
            if order.district not in my_delivery_object.based_on_district.all():
                messages.warning(
                    request, "You are not assigned for delivery in {}".format(order.district))
                return HttpResponseRedirect(reverse('delivery-order'))
            order.delivery_by = my_delivery_object
            order.delivery_taken_datetime = datetime.datetime.now()
            order.status = 2
            try:
                order.delivery_person_ip = request.new_ip.ip
            except Exception:
                pass
            order.save()

            messages.success(
                request, "You can deliver this order. Now it's your responsibility.")
            return redirect(order.get_detail_url())


@method_decorator(deliveryPerson_only, name='dispatch')
class CancelDelivery(LoginRequiredMixin, View):
    def get(self, request):
        orders = order_models.Order.cancelled_objects.all().order_by('-created_at')
        context = {}
        context.update({"orders": orders})
        context.update({"title": "Cancelled Orders"})
        return render(request, template_version+"/Views/Orders/cancelled.html", context=context)