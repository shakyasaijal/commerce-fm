from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import Group
from django.conf import settings


from User import models as user_models


if settings.MULTI_VENDOR:
    class Vendor(user_models.AbstractTimeStamp):
        organizationName = models.CharField(
            max_length=254, null=False, blank=False, verbose_name=_('Organization/ Vendor Name'))
        address = models.CharField(
            max_length=254, null=True, blank=True, verbose_name=_('Address'))
        vendorAdmin = models.ForeignKey(
            "User.User", on_delete=models.CASCADE, blank=False, null=False, related_name="vendorAdmin", verbose_name=_('Vendor Admin'))
        vendorUsers = models.ManyToManyField(
            "User.User", blank=True, related_name="vendorUsers")

        def __str__(self):
            return self.organizationName

        class Meta:
            verbose_name_plural = "Vendors"
            verbose_name = "Vendor"

    Group.add_to_class('vendor', models.ForeignKey(
        Vendor, on_delete=models.CASCADE, null=False, blank=False))

Group.add_to_class('description', models.TextField(
    null=True, blank=True, help_text="Help others to understand about this group."))
