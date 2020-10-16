import random
import string

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
