from django.db import models
from ckeditor.fields import RichTextField
import os
from django.utils.safestring import mark_safe
from django.dispatch import receiver
from datetime import datetime
from django.conf import settings

from User import models as user_models


if settings.HAS_OFFER_APP:
    class OfferCategory(user_models.AbstractTimeStamp):
        name = models.CharField(max_length=255, null=False, blank=False)

        def __str__(self):
            return self.name

        class Meta:
            verbose_name = "Category for Offers"
            verbose_name_plural = "Categories for Offers"

    def big_banner_image_name_change(instance, filename):
        upload_to = 'banners/big'
        ext = filename.split('.')[-1]
        # get filename
        file_extension = filename.split('.')[1]
        _datetime = datetime.now()
        datetime_str = _datetime.strftime("%Y-%m-%d-%H-%M-%S")
        date_format = datetime_str.split('-')
        date_join = ''.join(date_format)

        filename = '{}.{}'.format(date_join, ext)
        return os.path.join(upload_to, filename)

    def small_banner_image_name_change(instance, filename):
        upload_to = 'banners/small'
        ext = filename.split('.')[-1]
        # get filename
        file_extension = filename.split('.')[1]
        _datetime = datetime.now()
        datetime_str = _datetime.strftime("%Y-%m-%d-%H-%M-%S")
        date_format = datetime_str.split('-')
        date_join = ''.join(date_format)

        filename = '{}.{}'.format(date_join, ext)
        return os.path.join(upload_to, filename)

    class Offer(user_models.AbstractTimeStamp):
        title = models.CharField(max_length=255, null=False, blank=False)
        description = RichTextField(blank=True, null=True)
        starts_from = models.DateField(null=False, blank=False)
        ends_at = models.DateField(null=True, blank=True)
        big_banner_image = models.ImageField(
            upload_to=big_banner_image_name_change, blank=False)
        small_banner_image = models.ImageField(
            upload_to=small_banner_image_name_change, blank=False)
        category = models.ManyToManyField(
            OfferCategory, related_name="offers_category")

        if settings.MULTI_VENDOR:
            from Vendor import models as vendor_models
            vendor = models.ManyToManyField(
                vendor_models.Vendor, related_name="vendors_offer", help_text="Which vendors can participate?")

            def total_vendors(self):
                return self.vendor.count()

        def __str__(self):
            return self.title

        def big_banner_tag(self):
            try:
                return mark_safe('<img src="{}" width="150" height="150" />'.format(self.big_banner_image.url))
            except Exception as e:
                print(e)
        big_banner_tag.short_description = 'Big Banner'

        def small_banner_tag(self):
            try:
                return mark_safe('<img src="{}" width="150" height="150" />'.format(self.small_banner_image.url))
            except Exception as e:
                print(e)
        small_banner_tag.short_description = 'Small Banner'

        class Meta:
            verbose_name = "Special Offer"
            verbose_name_plural = "Special Offers"
            ordering = ["starts_from"]
            permissions = (
                ("participate_in_offer", "Can participate in offers."),
            )

    @receiver(models.signals.post_delete, sender=Offer)
    def auto_delete_file_on_delete(sender, instance, **kwargs):
        """
        Deletes file from filesystem
        when corresponding `MediaFile` object is deleted.
        """
        try:
            if sender.__name__ == 'Offer':
                if instance.big_banner_image:
                    if os.path.isfile(instance.big_banner_image.path):
                        os.remove(instance.big_banner_image.path)
                if instance.small_banner_image:
                    if os.path.isfile(instance.small_banner_image.path):
                        os.remove(instance.small_banner_image.path)

        except Exception as e:
            print('Delete on change', e)
            pass

    @receiver(models.signals.pre_save, sender=Offer)
    def auto_delete_file_on_change(sender, instance, **kwargs):
        """
        Deletes old file from filesystem
        when corresponding `MediaFile` object is updated
        with new file.
        """
        old_file = ""
        new_file = ""
        try:
            if sender.__name__ == "Offer":
                old_file = sender.objects.get(pk=instance.pk).big_banner_image
                new_file = instance.big_banner_image

                old_file1 = sender.objects.get(
                    pk=instance.pk).small_banner_image
                new_file1 = instance.small_banner_image

                if not old_file1 == new_file1:
                    if os.path.isfile(old_file1.path):
                        os.remove(old_file1.path)

        except sender.DoesNotExist:
            return False

        if not old_file == new_file:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)
