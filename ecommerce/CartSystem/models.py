from django.db import models
from User import models as user_models
from helper import modelHelper


class Location(models.Model):
    province = models.CharField(
        max_length=254, null=False, blank=False, default="Province 3")
    district = models.CharField(
        max_length=254, null=False, blank=False, default="Kathmandu")

    def __str__(self):
        return self.district


class WishList(user_models.AbstractTimeStamp):
    user = models.ForeignKey(user_models.User, null=False,
                             blank=False, on_delete=models.CASCADE)
    product = models.ForeignKey(
        "Products.Product", null=False, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.get_full_name()


class AddToCart(user_models.AbstractTimeStamp):
    user = models.ForeignKey(user_models.User, null=False,
                             blank=False, on_delete=models.CASCADE)
    product = models.ForeignKey(
        "Products.Product", null=False, blank=False, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return self.product.english_name


class OrderItem(user_models.AbstractTimeStamp):
    user = models.ForeignKey(user_models.User, on_delete=models.CASCADE)
    item = models.ForeignKey("Products.Product", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return "Quantity: {} {}, Product: {} - Rs. {}".format(self.quantity, self.item.sizes or '',
                                             self.item.english_name, self.item.price*self.quantity)


class Order(user_models.AbstractTimeStamp):
    item = models.ManyToManyField(OrderItem, blank=False)
    user = models.ForeignKey(user_models.User, null=True, blank=True, on_delete=models.PROTECT)
    status = models.IntegerField(choices=modelHelper.order_status_choice, null=False, blank=False, default=1)
    grand_total = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.user.get_full_name()

    def associated_name(self):
        return self.user.get_full_name()

class Delivery(user_models.AbstractTimeStamp):
    order = models.OneToOneField(Order, null=False, blank=False, on_delete=models.PROTECT)
    note = models.TextField(null=False, blank=False)
    location = models.ForeignKey(Location, null=False, blank=False, on_delete=models.PROTECT)

    def __str__(self):
        return self.order.user.get_full_name()
