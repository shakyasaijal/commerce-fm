from django.contrib import admin
from . import models


admin.site.register(models.Location)
admin.site.register(models.WishList)

class CartAdmin(admin.ModelAdmin):
    list_display = ['get_user_name']

admin.site.register(models.AddToCart, CartAdmin)
