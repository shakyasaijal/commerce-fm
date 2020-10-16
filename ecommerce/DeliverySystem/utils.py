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
    delivery_person = get_my_delivery_object(user)
    order = order_models.Order.objects.filter(Q(district__in=delivery_person.based_on_district.all()) | Q(direct_assign=delivery_person) & ~Q(status=3)).order_by('created_at', 'status')
    return order


def my_deliveries(user):
    delivery_person = get_my_delivery_object(user)
    order = order_models.Order.objects.filter(Q(direct_assign=delivery_person) | Q(delivery_by=delivery_person) & ~Q(status=3)).order_by('updated_at')
    return order


def my_daily_delivery(user):
    delivery_person = get_my_delivery_object(user)
    order = order_models.Order.objects.filter(Q(delivery_by=delivery_person) & Q(status=3)).extra(select={'day': 'date( delivery_taken_datetime )'}).values('day').annotate(total=Count('id')).values('day','total').order_by('updated_at')
    return order
