from django.contrib import admin
from . import models

admin.site.register(models.OrderItem)

class DeliveryInline(admin.TabularInline):
    model = models.Delivery
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ['associated_name', 'status', 'grand_total', 'created_at']
    inlines = [DeliveryInline,]
    list_filter = ('status', )
    search_fields = ['associated_name', 'status', 'grand_total']

admin.site.register(models.Order, OrderAdmin)