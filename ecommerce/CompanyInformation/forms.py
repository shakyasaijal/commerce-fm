from django import forms
from django.contrib import admin
from dal import autocomplete
from ckeditor.widgets import CKEditorWidget
from dal import autocomplete
from django.conf import settings

from helper import modelHelper
from CompanyInformation import models as company_models


class CompanyInfoForm(forms.ModelForm):
    email = forms.EmailField(required=False)
    phone = forms.ModelMultipleChoiceField(required=False, queryset=company_models.ContactNumber.objects.all(
    ), widget=autocomplete.ModelSelect2Multiple())
    address = forms.CharField(
        required=False, widget=forms.Textarea(attrs={"rows": 3, "cols": 10}))
    fax = forms.CharField(required=False)
    post_box = forms.CharField(required=False)

    class Meta:
        model = company_models.CompanyInformation
        fields = "__all__"


class SocialMediaForm(forms.ModelForm):
    facebook_link = forms.URLField(required=False)
    twitter_link = forms.URLField(required=False)
    linkedIn_link = forms.URLField(required=False)
    instagram_link = forms.URLField(required=False)
    youtube_link = forms.URLField(required=False)

    class Meta:
        model = company_models.SocialMedia
        fields = "__all__"


class ContactForm(forms.ModelForm):
    number = forms.IntegerField(required=True)
    of = forms.CharField(required=False)

    class Meta:
        model = company_models.ContactNumber
        fields = "__all__"
