from django import forms
from ckeditor.widgets import CKEditorWidget

from Products import models as products_models
from helper import modelHelper
from Vendor import models as vendor_models


class VendorRequestForm(forms.ModelForm):
    class Meta:
        model = vendor_models.VendorRequest
        fields = '__all__'
