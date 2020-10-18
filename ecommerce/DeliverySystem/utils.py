import random
import string
from django.db.models import Q, Count

from DeliverySystem import models as delivery_models
from OrderAndDelivery import models as order_models


def get_my_delivery_district(user):
    delivery = delivery_models.DeliveryPerson.objects.get(user=user)
    return delivery.based_on_district.all()


def get_my_delivery_object(user):
    try:
        return delivery_models.DeliveryPerson.objects.get(user=user)
    except (Exception, delivery_models.DeliveryPerson.DoesNotExist):
        return delivery_models.DeliveryPerson.objects.none()


def bill_number_generator(size=6, chars=string.ascii_uppercase + string.digits):
    def generate():
        generated = ''.join(random.choice(chars) for _ in range(size))
        return generated

    number = generate()
    while order_models.Order.objects.filter(bill_number=number).exists():
        number = generate()

    return number


def total_pending_orders(user):
    # All pending orders of my district or assigned to me.
    delivery_person = get_my_delivery_object(user)
    order = order_models.Order.objects.filter(Q(district__in=delivery_person.based_on_district.all()) | Q(
        direct_assign=delivery_person) & ~Q(status=3)).order_by('created_at', 'status')
    return order


def total_pending_admin():
    order = order_models.Order.objects.filter(
        ~Q(status=3)).order_by('created_at', 'status')
    return order


def my_deliveries(user):
    # Deliveries that I need to make
    delivery_person = get_my_delivery_object(user)
    order = order_models.Order.objects.filter(Q(direct_assign=delivery_person) | Q(
        delivery_by=delivery_person) & ~Q(status=3)).order_by('updated_at')
    return order


def my_daily_delivery(user):
    delivery_person = get_my_delivery_object(user)
    order = order_models.Order.objects.filter(Q(delivery_by=delivery_person) & Q(status=3)).extra(
        select={'day': 'date( delivery_taken_datetime )'}).annotate(total=Count('id')).values('day__date', 'total').order_by('-delivery_taken_datetime')
    return order


def orders_to_be_taken(user):
    # All orders that is not been taken
    delivery_person = get_my_delivery_object(user)
    order = order_models.Order.objects.filter(~Q(status=3) & Q(direct_assign__isnull=True) & Q(
        delivery_by__isnull=True) & Q(district__in=delivery_person.based_on_district.all())).order_by('created_at')
    return order


def orders_to_take_admin():
    order = order_models.Order.objects.filter(~Q(status=3) & Q(direct_assign__isnull=True) & Q(
        delivery_by__isnull=True)).order_by('created_at')
    return order


def cancelled_orders(user):
    delivery_person = get_my_delivery_object(user)
    order = order_models.Order.cancelled_objects.filter(
        Q(district__in=delivery_person.based_on_district.all()) | Q(direct_assign=delivery_person)).order_by('-created_at')
    return order


def cancelled_order_admin():
    order = order_models.Order.cancelled_objects.all()
    return order


def index_data(user):
    context = {}
    if not user.is_superuser:
        my_deliveries_data = my_deliveries(user)
        total_pending_orders_data = total_pending_orders(user)
        orders_to_be_taken_data = orders_to_be_taken(user)
        cancelled_data = cancelled_orders(user)

        context.update({"my_deliveries": my_deliveries_data})
        context.update({"total_pending_orders": total_pending_orders_data})
        context.update({"orders_to_be_taken": orders_to_be_taken_data})
        context.update({"cancelled_orders": cancelled_data})
    else:
        total_pending_admin_data = total_pending_admin()
        order_to_take_admin_data = orders_to_take_admin()
        cancelled_data = cancelled_order_admin()
        
        context.update({"total_pending_admin": total_pending_admin_data})
        context.update({"order_to_take_admin": order_to_take_admin_data})
        context.update({"cancelled_orders": cancelled_data})

    return context
