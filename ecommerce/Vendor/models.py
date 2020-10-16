from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import Group
from django.conf import settings


from User import models as user_models
from helper import modelHelper


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
        phone = models.CharField(max_length=255, null=False, blank=False, default="None")

        def __str__(self):
            return self.organizationName

        class Meta:
            verbose_name_plural = "Vendors"
            verbose_name = "Vendor"

    class VendorRequest(user_models.AbstractTimeStamp):
        email = models.EmailField(
            max_length=255, null=False, blank=False, unique=True)
        organizationName = models.CharField(
            max_length=254, null=False, blank=False, verbose_name=_('Organization/ Vendor Name'), unique=True)
        first_name = models.CharField(max_length=100, null=False, blank=False)
        last_name = models.CharField(max_length=100, null=False, blank=False)

        def __str__(self):
            return self.organizationName

        def get_full_name(self):
            return self.first_name+" "+self.last_name

        class Meta:
            verbose_name = "Vendor Request"
            verbose_name_plural = "Vendor Requests"

    class NoticeToVendors(user_models.AbstractTimeStamp):
        title = models.CharField(max_length=255, null=False, blank=False)
        description = models.TextField(null=False, blank=False)
        vendors = models.ManyToManyField(Vendor, blank=False)
        display = models.BooleanField(
            null=False, blank=False, default=True, choices=modelHelper.notice_status)
        importance = models.IntegerField(null=False, blank=False, choices=modelHelper.importance_status, default=3)

    Group.add_to_class('vendor', models.ForeignKey(
        Vendor, on_delete=models.CASCADE, null=False, blank=False))

Group.add_to_class('description', models.TextField(
    null=True, blank=True, help_text="Help others to understand about this group."))
