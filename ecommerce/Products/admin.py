from django.contrib import admin
from . import models

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['english_name', 'isFeatured']
    readonly_fields = ['image_tag']


class ProductImageInline(admin.TabularInline):
    model = models.ProductImage
    extra = 4
    readonly_fields = ['image_tag']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['english_name', 'status', 'is_featured']
    inlines = [ ProductImageInline, ]
    list_filter = ("status",)
    search_fields = ['english_name', 'price', 'old_price', 'description', 'sizes']
    readonly_fields = ['image_tag']


admin.site.register(models.Size)
admin.site.register(models.Tags)
admin.site.register(models.Brand)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Product, ProductAdmin)
