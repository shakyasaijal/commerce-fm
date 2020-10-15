from django.contrib import admin
from . import models

admin.site.register(models.OrderItem)


class OrderAdmin(admin.ModelAdmin):
    list_display = ['associated_name', 'status', 'grand_total', 'created_at']
    list_filter = ('status', )
    search_fields = ['associated_name', 'status', 'grand_total']

admin.site.register(models.Order, OrderAdmin)