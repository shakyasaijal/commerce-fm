from django.db import models
from django.db.models import Q
from django.conf import settings

from User import models as user_models
from helper import modelHelper
from CartSystem import models as cart_models


class OrderItem(user_models.AbstractTimeStamp):
    user = models.ForeignKey(user_models.User, on_delete=models.CASCADE)
    item = models.ForeignKey("Products.Product", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, null=False, blank=False)

    def __str__(self):
        return "Quantity: {} {}, Product: {} - Rs. {}".format(self.quantity, self.item.sizes or '',
                                                              self.item.english_name, self.item.price*self.quantity)


class DeliveredManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=3).order_by('created_at')


class PaymentMethods(user_models.AbstractTimeStamp):
    method = models.CharField(max_length=255, null=False, blank=False)
    count = models.BigIntegerField(null=False, blank=False, default=0)

    def __str__(self):
        return self.method

    class Meta:
        ordering = ['-count']
        verbose_name = "Payment Method"
        verbose_name_plural = "Payment Methods"


class Order(user_models.AbstractTimeStamp):
    deliver_to_choice = (
        (True, "Self"),
        (False, "Other"),
    )

    payment_status_choice = (
        ("1", "Pending"),
        ("2", "Online Transfered/ Online Payment"),
        ("3", "Cash In Hand")
    )

    item = models.ManyToManyField(
        OrderItem, blank=False, related_name="order_orderItem")
    user = models.ForeignKey(user_models.User, null=False,
                             blank=False, on_delete=models.PROTECT)
    status = models.IntegerField(
        choices=modelHelper.order_status_choice, null=False, blank=False, default=1)
    grand_total = models.FloatField(null=True, blank=True)

    # To identify where to deliver
    deliver_to = models.BooleanField(
        null=False, blank=False, default=True, choices=deliver_to_choice)

    # IF deliver_to == False
    other_full_name = models.CharField(max_length=255, null=True, blank=True)
    other_phone = models.CharField(max_length=255, null=True, blank=True)
    other_address = models.TextField(null=True, blank=True)
    payment_by = models.BooleanField(
        null=False, blank=False, default=True, choices=deliver_to_choice)

    # Is Required for self and other
    district = models.ForeignKey(
        'CartSystem.Location', null=False, blank=False, on_delete=models.CASCADE)

    direct_assign = models.ForeignKey(
        'DeliverySystem.DeliveryPerson', on_delete=models.CASCADE, null=True, blank=True, related_name="order_assigned")

    any_info = models.TextField(null=True, blank=True)

    payment_method = models.ForeignKey(
        PaymentMethods, on_delete=models.PROTECT, null=False, blank=False)
    payment_status = models.CharField(
        max_length=100, null=False, blank=False, default="1", choices=payment_status_choice)

    # If direct assign, then delivery_by = direct_assign
    delivery_by = models.ForeignKey("DeliverySystem.DeliveryPerson", null=True, blank=True, on_delete=models.PROTECT, related_name='order_delivery_person')

    objects = models.Manager()
    delivered_objects = DeliveredManager()

    def __str__(self):
        return self.user.get_full_name()

    def associated_name(self):
        return self.user.get_full_name()
