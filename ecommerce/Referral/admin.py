from django.conf import settings
from django.contrib import admin
from . import models


if settings.HAS_REFERRAL_APP:
    class ReferAdmin(admin.ModelAdmin):
        list_display = ['user_full_name', 'refer_code']
        search_fields = ['user_full_name', 'refer_code']

    class RewardAdmin(admin.ModelAdmin):
        list_display = ['user_full_name']

    class BlockAdmin(admin.ModelAdmin):
        list_display = ['data_hash', 'previous_hash', 'genesis_block']

    admin.site.register(models.Referral, ReferAdmin)
    admin.site.register(models.Reward, RewardAdmin)
    admin.site.register(models.Block, BlockAdmin)


if settings.HAS_VENDOR_REFERRAL_APP:
    class VendorReferAdmin(admin.ModelAdmin):
        list_display = ['vendor_name', 'refer_code']
        search_fields = ['vendor_name', 'refer_code']

    class VendorRewardAdmin(admin.ModelAdmin):
        list_display = ['vendor_name']

    class VendorBlockAdmin(admin.ModelAdmin):
        list_display = ['data_hash', 'previous_hash', 'genesis_block']

    admin.site.register(models.VendorReferral, VendorReferAdmin)
    admin.site.register(models.VendorReward, VendorRewardAdmin)
    admin.site.register(models.VendorBlock, VendorBlockAdmin)
    admin.site.register(models.VendorKey)