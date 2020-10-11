from django.conf import settings
from django.db import models

from User import models as user_models
from helper import modelHelper


if settings.HAS_REFERRAL_APP:
    class Referral(user_models.AbstractTimeStamp):
        user = models.OneToOneField(
            user_models.User, on_delete=models.CASCADE, null=False, blank=False)
        refer_code = models.CharField(max_length=255, null=False, blank=False)
        refer_url = models.URLField(null=False, blank=False, default='')

        def __str__(self):
            return self.user.get_full_name()

        class Meta:
            verbose_name = "Referral Activation"
            verbose_name_plural = "Referral Activations"

        def user_full_name(self):
            return self.user.get_full_name()

    class Reward(user_models.AbstractTimeStamp):
        referral = models.ForeignKey(Referral, on_delete=models.CASCADE)
        points = models.BigIntegerField(null=False, blank=False, default=0)
        visited = models.BigIntegerField(null=False, blank=False, default=0)
        signed_up = models.BigIntegerField(null=False, blank=False, default=0)
        buyed = models.BigIntegerField(null=False, blank=False, default=0)

        def __str__(self):
            return "{} -> {}".format(self.referral.user
                                     .get_full_name(), self.points)

        class Meta:
            verbose_name = "Reward"
            verbose_name_plural = "Rewards"

        def user_full_name(self):
            return self.referral.user_full_name()

    class UserKey(user_models.AbstractTimeStamp):
        key = models.CharField(max_length=255, null=False,
                               blank=False, unique=True)
        referredFrom = models.ForeignKey(Referral, on_delete=models.CASCADE)

        def __str__(self):
            return "Key: {}".format(self.key)

    class Block(user_models.AbstractTimeStamp):
        data = models.CharField(max_length=255, null=False, blank=False)
        data_hash = models.CharField(
            max_length=255, null=False, blank=False, unique=True)
        previous_has = models.TextField(
            null=False, blank=False, default="00xx00")
        genesis_block = models.BooleanField(
            null=False, blank=False, choices=modelHelper.genesis_block, default=False)

        # IF GENESIS BLOCK
        user = models.ForeignKey(
            "User.User", on_delete=models.DO_NOTHING, null=True, blank=True)

        def __str__(self):
            return self.data


if settings.HAS_VENDOR_REFERRAL_APP:
    class VendorReferral(user_models.AbstractTimeStamp):
        vendor = models.OneToOneField("Vendor.Vendor", null=False, blank=False, on_delete=models.CASCADE)
        refer_code = models.CharField(max_length=255, null=False, blank=False)
        refer_url = models.URLField(null=False, blank=False, default='')

        def __str__(self):
            return self.vendor.organizationName

        class Meta:
            verbose_name = "Vendor Referral Activation"
            verbose_name_plural = "Vendor Referral Activations"

        def vendor_name(self):
            return self.vendor.organizationName

    class VendorReward(user_models.AbstractTimeStamp):
        referral = models.ForeignKey(VendorReferral, on_delete=models.CASCADE)
        points = models.BigIntegerField(null=False, blank=False, default=0)
        visited = models.BigIntegerField(null=False, blank=False, default=0)
        signed_up = models.BigIntegerField(null=False, blank=False, default=0)
        buyed = models.BigIntegerField(null=False, blank=False, default=0)

        def __str__(self):
            return "{} -> {}".format(self.referral.vendor_name(), self.points)

        class Meta:
            verbose_name = "Vendor Reward"
            verbose_name_plural = "Vendor Rewards"

        def user_full_name(self):
            return self.referral.vendor_name()

    class VendorKey(user_models.AbstractTimeStamp):
        key = models.CharField(max_length=255, null=False,
                               blank=False, unique=True)
        referredFrom = models.ForeignKey(
            VendorReferral, on_delete=models.CASCADE)

        def __str__(self):
            return "Key: {}".format(self.key)

    class VendorBlock(user_models.AbstractTimeStamp):
        data = models.CharField(max_length=255, null=False, blank=False)
        data_hash = models.CharField(
            max_length=255, null=False, blank=False, unique=True)
        previous_has = models.TextField(
            null=False, blank=False, default="00xx00")
        genesis_block = models.BooleanField(
            null=False, blank=False, choices=modelHelper.genesis_block, default=False)

        # IF GENESIS BLOCK
        user = models.ForeignKey(
            "Vendor.Vendor", on_delete=models.DO_NOTHING, null=True, blank=True)

        def __str__(self):
            return self.data

