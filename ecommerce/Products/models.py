from django.db import models
import os
from django.utils.safestring import mark_safe
from django.dispatch import receiver
from datetime import datetime
from django.conf import settings
from ckeditor.fields import RichTextField

from helper import modelHelper
from User import models as user_models


def category_image_name_change(instance, filename):
    upload_to = 'category-image'
    ext = filename.split('.')[-1]
    # get filename
    file_extension = filename.split('.')[1]
    _datetime = datetime.now()
    datetime_str = _datetime.strftime("%Y-%m-%d-%H-%M-%S")
    date_format = datetime_str.split('-')
    date_join = ''.join(date_format)

    filename = '{}.{}'.format(date_join, ext)
    return os.path.join(upload_to, filename)


def product_image_name_change(instance, filename):
    upload_to = 'product-image'
    ext = filename.split('.')[-1]
    # get filename
    file_extension = filename.split('.')[1]
    _datetime = datetime.now()
    datetime_str = _datetime.strftime("%Y-%m-%d-%H-%M-%S")
    date_format = datetime_str.split('-')
    date_join = ''.join(date_format)

    filename = '{}.{}'.format(date_join, ext)
    return os.path.join(upload_to, filename)


class Category(user_models.AbstractTimeStamp):
    english_name = models.CharField(max_length=250, null=False,
                                    blank=False, unique=True)
    nepali_name = models.CharField(max_length=250, null=False,
                                   blank=False, unique=True)
    categoryImage = models.ImageField(
        upload_to=category_image_name_change, null=False, blank=False, verbose_name="Category Image")
    isFeatured = models.BooleanField(
        null=False, blank=False, default=False, choices=modelHelper.is_featured, verbose_name="Is a featured product?")

    def __str__(self):
        return self.english_name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def image_tag(self):
        try:
            return mark_safe('<img src="{}" width="150" height="150" />'.format(self.categoryImage.url))
        except Exception as e:
            print(e)
    image_tag.short_description = 'Image'


class Tags(user_models.AbstractTimeStamp):
    tag = models.CharField(max_length=200, null=False, blank=False)

    def __str__(self):
        return self.tag

    class Meta:
        verbose_name_plural = "Tags"


class Size(user_models.AbstractTimeStamp):
    size = models.CharField(max_length=255, null=False,
                            blank=False, unique=True)

    def __str__(self):
        return self.size

    def save(self, *args, **kwargs):
        self.size = self.size.lower()
        super(Size, self).save(*args, **kwargs)


class Brand(user_models.AbstractTimeStamp):
    name = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return self.name


class ProductManager(models.Manager):
    def get_queryset(self):
        if not settings.DISPLAY_OUT_OF_STOCK_PRODUCTS:
            return super().get_queryset().filter(soft_delete=False, status=True)
        return super().get_queryset().filter(soft_delete=False)


class Product(user_models.AbstractTimeStamp):
    english_name = models.CharField(max_length=255, null=False, blank=False)
    nepali_name = models.CharField(max_length=255, null=True, blank=True)
    old_price = models.FloatField(max_length=255, null=True, blank=True)
    price = models.FloatField(max_length=255, null=False, blank=False)
    short_description = RichTextField(
        help_text="Not more than 30 words.", blank=True, null=True)
    description = RichTextField(
        help_text="Bio e.g. size, material type, etc", blank=True, null=True)
    category = models.ManyToManyField(
        Category, related_name="category_product",  blank=True)
    quantity_left = models.BigIntegerField(
        null=True, blank=True, default=0, help_text="Automatic quantity decreased after order placed. Leave it empty for unlimited/manual quantity of the product.")
    status = models.BooleanField(choices=modelHelper.availability_choice, null=False, blank=False,
                                 default=True, help_text="Status with Available are only visible in the site.")
    is_featured = models.BooleanField(
        null=False, blank=False, default=False, choices=modelHelper.is_featured)
    tags = models.ManyToManyField(
        Tags, related_name="product_tags", blank=True)
    sizes = models.ManyToManyField(Size, blank=True)
    brand_name = models.ForeignKey(
        Brand, related_name='brand', blank=True, null=True, on_delete=models.CASCADE)
    warranty = models.CharField(
        max_length=255, blank=True, help_text="eg: 1 year or 6 months")
    main_image = models.ImageField(
        upload_to=product_image_name_change, blank=False)
    related_products = models.ManyToManyField(
        'self', blank=True, related_name='related_products')
    soft_delete = models.BooleanField(
        choices=modelHelper.soft_delete, null=False, blank=False, default=False)
    objects = ProductManager()
    deletedObject = models.Manager()

    if settings.MULTI_VENDOR:
        vendor = models.ForeignKey(
            'Vendor.Vendor', on_delete=models.CASCADE, null=False, blank=False)

    if settings.HAS_OFFER_APP:
        offers = models.ManyToManyField(
            "Offer.OfferCategory", related_name="offer_products", blank=True)

    def __str__(self):
        return self.english_name

    def image_tag(self):
        try:
            return mark_safe('<img src="{}" width="150" height="150" />'.format(self.main_image.url))
        except Exception as e:
            print(e)
    image_tag.short_description = 'Main Image'

    def delete_softly(self):
        self.soft_delete = not self.soft_delete

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"


class SoftDeletedProducts(Product):
    class Meta:
        proxy = True
        verbose_name = "Deleted Product"
        verbose_name_plural = "Deleted Products"


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, related_name='product_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=product_image_name_change, blank=True)

    def __str__(self):
        return self.product.english_name

    def image_tag(self):
        try:
            return mark_safe('<img src="{}" width="150" height="150" />'.format(self.image.url))
        except Exception as e:
            pass

    image_tag.short_description = 'Image'


@receiver(models.signals.post_delete, sender=Category)
@receiver(models.signals.post_delete, sender=Product)
@receiver(models.signals.post_delete, sender=ProductImage)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    try:
        if sender.__name__ == 'Category':
            if instance.categoryImage:
                if os.path.isfile(instance.categoryImage.path):
                    os.remove(instance.categoryImage.path)

        if sender.__name__ == 'Product':
            if instance.main_image:
                if os.path.isfile(instance.main_image.path):
                    os.remove(instance.main_image.path)

        if sender.__name__ == 'ProductImage':
            if instance.image:
                if os.path.isfile(instance.image.path):
                    os.remove(instance.image.path)

    except Exception as e:
        print('Delete on change', e)
        pass


@receiver(models.signals.pre_save, sender=Category)
@receiver(models.signals.pre_save, sender=Product)
@receiver(models.signals.pre_save, sender=ProductImage)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    old_file = ""
    new_file = ""
    try:
        if sender.__name__ == "Category":
            old_file = sender.objects.get(pk=instance.pk).categoryImage
            new_file = instance.categoryImage

        if sender.__name__ == "Product":
            old_file = sender.objects.get(pk=instance.pk).main_image
            new_file = instance.main_image

        if sender.__name__ == "ProductImage":
            old_file = sender.objects.get(pk=instance.pk).image
            new_file = instance.image

    except sender.DoesNotExist:
        return False

    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
