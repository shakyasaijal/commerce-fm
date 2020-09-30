from django.contrib import admin
from django.conf import settings
from . import models

class VendorAdmin(admin.ModelAdmin):
    list_display = ('organizationName', 'address', 'vendorAdmin') 
    search_fields = ['organizationName', 'address']

if settings.MULTI_VENDOR:
    admin.site.register(models.Vendor, VendorAdmin)
    admin.site.register(models.VendorRequest)