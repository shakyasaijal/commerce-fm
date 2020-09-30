from django.contrib import admin
from django.conf import settings
from django.contrib.admin.models import LogEntry, DELETION
from . import models
from django.utils.html import escape
from django.urls import reverse
from django.utils.safestring import mark_safe


class VendorAdmin(admin.ModelAdmin):
    list_display = ('organizationName', 'address', 'vendorAdmin') 
    search_fields = ['organizationName', 'address']

if settings.MULTI_VENDOR:
    admin.site.register(models.Vendor, VendorAdmin)
    admin.site.register(models.VendorRequest)


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'action_time'

    list_filter = [
        'user',
        'content_type',
        'action_flag'
    ]

    search_fields = [
        'object_repr',
        'change_message'
    ]

    list_display = [
        'action_time',
        'user',
        'content_type',
        'action_flag',
    ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    # def object_link(self, obj):
    #     if obj.action_flag == DELETION:
    #         link = escape(obj.object_repr)
    #     else:
    #         ct = obj.content_type
    #         link = '<a href="%s">%s</a>' % (
    #             reverse('admin:%s_%s_change' % (ct.app_label, ct.model), args=[obj.object_id]),
    #             escape(obj.object_repr),
    #         )
    #     return mark_safe(link)
    # object_link.admin_order_field = "object_repr"
    # object_link.short_description = "object"