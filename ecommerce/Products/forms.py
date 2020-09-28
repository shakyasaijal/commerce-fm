from django import forms
from Products import models as products_models
from ckeditor.widgets import CKEditorWidget
from helper import modelHelper


class CategoryForm(forms.ModelForm):
    class Meta:
        model = products_models.Category
        fields ="__all__"

    english_name = forms.CharField(max_length=255)
    nepali_name = forms.CharField(max_length=255)
    categoryImage = forms.ImageField(label="Category Image")
    isFeatured = forms.ChoiceField(required=False, choices=modelHelper.is_featured, label="Is a featured product?")


class ProductForm(forms.ModelForm):
    class Meta:
        model = products_models.Product
        fields = "__all__"

    english_name = forms.CharField(max_length=254)
    nepali_name = forms.CharField(max_length=254)
    old_price = forms.CharField(required=False, max_length=254)
    price = forms.CharField(max_length=254)
    description = forms.CharField(label='Description', help_text="eg: size, material type, color etc", widget=CKEditorWidget(),required=False)
    short_description = forms.CharField(label='Short Bio', help_text="eg: size, material type, color etc", widget=CKEditorWidget(),required=False)
    category = forms.ModelMultipleChoiceField(required=False, queryset=products_models.Category.objects.all())
    status = forms.ChoiceField(required=False, choices=modelHelper.availability_choice)
    is_featured = forms.ChoiceField(required=False, choices=modelHelper.is_featured)
    tags = forms.ModelMultipleChoiceField(required=False, queryset=products_models.Tags.objects.all())
    sizes = forms.ModelMultipleChoiceField(required=False, queryset=products_models.Size.objects.all())
    brand_name = forms.ModelChoiceField(required=False, queryset=products_models.Brand.objects.all())
    warranty = forms.CharField(required=False, max_length=254,  help_text="eg: 1 year or 6 months")
    main_image = forms.ImageField(label='Main/ Cover Image')
    related_products = forms.ModelMultipleChoiceField(required=False, queryset=products_models.Product.objects.all(),  help_text="Similar products that you sell")

    def __init__(self, vendor, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['related_products'].queryset = products_models.Product.objects.filter(vendor = vendor)


class ProductSingleForm(forms.ModelForm):
    class Meta:
        model = products_models.Product
        fields ="__all__"

    english_name = forms.CharField(max_length=254)
    nepali_name = forms.CharField(max_length=254)
    old_price = forms.CharField(required=False, max_length=254)
    price = forms.CharField(max_length=254)
    description = forms.CharField(label='Description', help_text="eg: size, material type, color etc", widget=CKEditorWidget(),required=False)
    short_description = forms.CharField(label='Short Bio', help_text="eg: size, material type, color etc", widget=CKEditorWidget(),required=False)
    category = forms.ModelMultipleChoiceField(required=False, queryset=products_models.Category.objects.all())
    status = forms.ChoiceField(required=False, choices=modelHelper.availability_choice)
    is_featured = forms.ChoiceField(required=False, choices=modelHelper.is_featured)
    tags = forms.ModelMultipleChoiceField(required=False, queryset=products_models.Tags.objects.all())
    sizes = forms.ModelMultipleChoiceField(required=False, queryset=products_models.Size.objects.all())
    brand_name = forms.ModelChoiceField(required=False, queryset=products_models.Brand.objects.all())
    warranty = forms.CharField(required=False, max_length=254,  help_text="eg: 1 year or 6 months")
    main_image = forms.ImageField(label='Main/ Cover Image')
    related_products = forms.ModelMultipleChoiceField(required=False, queryset=products_models.Product.objects.all(),  help_text="Similar products that you sell")


class ProductImage(forms.ModelForm):
    image = forms.ImageField(label='Image')
    class Meta:
        model = products_models.ProductImage
        fields = ('image',)


# class CommentForm(forms.ModelForm):
#     body = forms.CharField(
#         widget=forms.TextInput(attrs={
#             'placeholder': 'Enter Reply Here ...'
#         })
#     )
#     class Meta:
#         model = products_models.Comment
#         fields = ('body',)