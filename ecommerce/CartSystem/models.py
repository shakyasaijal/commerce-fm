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

    def get_user_name(self):
        return self.user.get_full_name()
