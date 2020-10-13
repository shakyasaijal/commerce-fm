from django.contrib import admin
from django.conf import settings

from . import models

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['english_name', 'isFeatured']
    readonly_fields = ['image_tag']
    search_fields = ['english_name', 'nepali_name']


class ProductImageInline(admin.TabularInline):
    model = models.ProductImage
    extra = 4
    readonly_fields = ['image_tag']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['english_name', 'status', 'is_featured', 'soft_delete']
    inlines = [ ProductImageInline, ]
    list_filter = ("status",)
    search_fields = ['english_name', 'price', 'old_price', 'description', 'sizes']
    readonly_fields = ['image_tag']
    list_per_page = 25
    

@admin.register(models.SoftDeletedProducts)
class DeletedProductsAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return self.model.deletedObject.filter(soft_delete=True)

    list_per_page = 25
    list_display = ['english_name', 'is_featured', 'status']
    search_fields = ['english_name', 'price', 'old_price', 'description', 'sizes']



admin.site.register(models.Size)
admin.site.register(models.Tags)
admin.site.register(models.Brand)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Comment)


if settings.MULTI_VENDOR:
    admin.site.register(models.NewCategoryRequest)
