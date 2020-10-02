from django import forms
from django.contrib import admin
from dal import autocomplete
from ckeditor.widgets import CKEditorWidget
from django.conf import settings

from helper import modelHelper
from Products import models as products_models
from Vendor import models as vendor_models

if settings.HAS_OFFER_APP:
    from Offer import models as offer_models


class CategoryForm(forms.ModelForm):
    class Meta:
        model = products_models.Category
        fields = "__all__"

    english_name = forms.CharField(max_length=255)
    nepali_name = forms.CharField(max_length=255)
    categoryImage = forms.ImageField(label="Category Image")
    isFeatured = forms.ChoiceField(
        required=False, choices=modelHelper.is_featured, label="Is a featured product?")


class ProductForm(forms.ModelForm):
    class Meta:
        model = products_models.Product
        fields = "__all__"

    english_name = forms.CharField(
        max_length=254, widget=forms.TextInput(attrs={'autoFocus': True}))
    nepali_name = forms.CharField(max_length=254)
    old_price = forms.FloatField(required=False)
    price = forms.FloatField(required=True)
    description = forms.CharField(
        label='Description', widget=CKEditorWidget(), required=False)
    short_description = forms.CharField(
        label='Short Bio', help_text="Eg: size, material type, color etc", widget=CKEditorWidget(), required=False)
    category = forms.ModelMultipleChoiceField(
        required=False, queryset=products_models.Category.objects.all(), widget=autocomplete.ModelSelect2Multiple())
    status = forms.ChoiceField(required=False, choices=modelHelper.availability_choice,
                               help_text="Status with Available are only visible in the site.")
    is_featured = forms.ChoiceField(required=False, choices=modelHelper.is_featured,
                                    help_text="Featured Product will be displayed in homepage.")
    tags = forms.ModelMultipleChoiceField(required=False, queryset=products_models.Tags.objects.all(
    ), widget=autocomplete.ModelSelect2Multiple(), help_text="Tags will be used for search engine.")
    sizes = forms.ModelMultipleChoiceField(required=False, queryset=products_models.Size.objects.all(
    ), widget=autocomplete.ModelSelect2Multiple())
    brand_name = forms.ModelChoiceField(
        required=False, queryset=products_models.Brand.objects.all(), widget=autocomplete.ModelSelect2())
    warranty = forms.CharField(
        required=False, max_length=254,  help_text="eg: 1 year or 6 months")
    main_image = forms.ImageField(label='Main/ Cover Image')
    related_products = forms.ModelMultipleChoiceField(required=False, queryset=products_models.Product.objects.all(
    ),  help_text="Similar products that you sell", widget=autocomplete.ModelSelect2Multiple())
    quantity_left = forms.IntegerField(
        required=False, help_text="Automatic quantity decreased after order placed. Leave it empty for unlimited/manual quantity of the product.")
    vendor = forms.ModelChoiceField(
        required=False, queryset=products_models.ProductImage.objects.none())
    soft_delete = forms.ChoiceField(required=False)

    if settings.HAS_OFFER_APP:
        offer = forms.ModelMultipleChoiceField(required=False, queryset=offer_models.OfferCategory.objects.all())

    def __init__(self, vendor, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['related_products'].queryset = products_models.Product.objects.filter(
            vendor=vendor)


class ProductSingleForm(forms.ModelForm):
    class Meta:
        model = products_models.Product
        fields = "__all__"

    english_name = forms.CharField(max_length=254)
    nepali_name = forms.CharField(max_length=254)
    old_price = forms.CharField(required=False, max_length=254)
    price = forms.CharField(max_length=254)
    description = forms.CharField(
        label='Description', widget=CKEditorWidget(), required=False)
    short_description = forms.CharField(
        label='Short Bio', help_text="Eg: size, material type, color etc", widget=CKEditorWidget(), required=False)
    category = forms.ModelMultipleChoiceField(
        required=False, queryset=products_models.Category.objects.all(), widget=autocomplete.ModelSelect2Multiple())
    status = forms.ChoiceField(required=False, choices=modelHelper.availability_choice,
                               help_text="Status with Available are only visible in the site.")
    is_featured = forms.ChoiceField(required=False, choices=modelHelper.is_featured,
                                    help_text="Featured Product will be displayed in homepage.")
    tags = forms.ModelMultipleChoiceField(required=False, queryset=products_models.Tags.objects.all(
    ), help_text="Tags will be used for search engine.")
    sizes = forms.ModelMultipleChoiceField(required=False, queryset=products_models.Size.objects.all(
    ), widget=autocomplete.ModelSelect2Multiple())
    brand_name = forms.ModelChoiceField(
        required=False, queryset=products_models.Brand.objects.all(), widget=autocomplete.ModelSelect2())
    warranty = forms.CharField(
        required=False, max_length=254,  help_text="eg: 1 year or 6 months")
    main_image = forms.ImageField(label='Main/ Cover Image')
    related_products = forms.ModelMultipleChoiceField(required=False, queryset=products_models.Product.objects.all(
    ),  help_text="Similar products that you sell", widget=autocomplete.ModelSelect2Multiple())
    soft_delete = forms.ChoiceField(required=False)

    if settings.HAS_OFFER_APP:
        offer = forms.ModelMultipleChoiceField(required=False, queryset=offer_models.OfferCategory.objects.all())

class ProductImage(forms.ModelForm):
    image = forms.ImageField(label='Image')

    class Meta:
        model = products_models.ProductImage
        fields = ('image',)
