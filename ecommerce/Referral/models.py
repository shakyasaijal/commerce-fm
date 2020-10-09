from django.conf import settings
from django.db import models

from User import models as user_models


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
        referral = models.ForeignKey(Referral, on_delete=models.DO_NOTHING)
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
