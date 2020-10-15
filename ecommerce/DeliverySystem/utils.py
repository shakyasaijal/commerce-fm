from DeliverySystem import models as delivery_models


def get_my_delivery_district(user):
    delivery = delivery_models.DeliveryPerson.objects.get(user=user)
    return delivery.based_on_district.all()

def get_my_delivery_object(user):
    try:
        return delivery_models.DeliveryPerson.objects.get(user=user)
    except (Exception, delivery_models.DeliveryPerson.DoesNotExist):
        return delivery_models.DeliveryPerson.objects.none()