from django.conf import settings
from django.contrib import admin
from . import models


if settings.HAS_REFERRAL_APP:
    class ReferAdmin(admin.ModelAdmin):
        list_display = ['user_full_name', 'refer_code']
        search_fields = ['user_full_name', 'refer_code']

    class RewardAdmin(admin.ModelAdmin):
        list_display = ['user_full_name']

    admin.site.register(models.Referral, ReferAdmin)
    admin.site.register(models.Reward, RewardAdmin)
