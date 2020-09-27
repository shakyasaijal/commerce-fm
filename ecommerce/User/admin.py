from django.contrib import admin
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from . import models


class UserAdmin(admin.ModelAdmin):
    list_display = ['get_full_name', 'email', 'is_verified']
    search_fields = ['get_full_name', 'email', 'date_joined', 'username']
    list_filter = ('groups',)

    def save_model(self, request, obj, form, change):
        if 'password' in form.changed_data:
            obj.set_password(request.POST['password'])
        obj.save()

admin.site.register(models.User, UserAdmin)


if settings.MULTI_VENDOR:
    try:
        class UserProfileAdmin(admin.ModelAdmin):
            list_display = ['associated_user', 'phone', 'address']
            search_fields = ['associated_user', 'phone', 'address']

        admin.site.register(models.UserProfile, UserProfileAdmin)
    except (Exception, KeyError) as e:
        raise ImproperlyConfigured("User/admin.py:: Multi Vendor is turned on.")
