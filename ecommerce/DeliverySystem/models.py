from django.db import models

from User import models as user_models
from CartSystem import models as cart_models


class DeliveryPerson(user_models.AbstractTimeStamp):
    user = models.OneToOneField(
        user_models.User, on_delete=models.PROTECT, null=False, blank=False)
    based_on_district = models.ManyToManyField(
        cart_models.Location, related_name="delivery_district", blank=True)

    def __str__(self):
        return self.user.get_full_name()
