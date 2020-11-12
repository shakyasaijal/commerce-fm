from django import forms
from django.contrib import admin
from dal import autocomplete
from ckeditor.widgets import CKEditorWidget
from django.conf import settings

from helper import modelHelper
from Products import models as products_models
from Vendor import models as vendor_models
from Offer import models as offer_models


class OfferForm(forms.ModelForm):
    class Meta:
        model = offer_models.Offer
        fields = "__all__"

    title = forms.CharField(max_length=255, required=True,
                            widget=forms.TextInput(attrs={'autoFocus': True}))
    description = forms.CharField(
        label='Description', widget=CKEditorWidget(), required=False)
    starts_from = forms.DateField(
        required=True)
    ends_at = forms.DateField(required=False)
    big_banner_image = forms.ImageField(required=True, label="Big Banner Image",
                                        help_text="Please provide good quality image with size of 1200*350.")
    small_banner_image = forms.ImageField(
        required=True, label="Small Banner Image", help_text="Please provide good quality image with size of 800*150.")
    category = forms.ModelMultipleChoiceField(
        required=True, queryset=offer_models.OfferCategory.objects.all(), widget=autocomplete.ModelSelect2Multiple(), help_text="What category can be included?")
    discounts = forms.CharField(
        label='Discount', help_text='Add Discounts with Comma Seperated',
        widget=forms.TextInput(attrs={'autoFocus': True}))

    if settings.MULTI_VENDOR:
        vendor = forms.ModelMultipleChoiceField(
            required=True, queryset=vendor_models.Vendor.objects.all(), widget=autocomplete.ModelSelect2Multiple(), help_text="Which vendors can participate?")
