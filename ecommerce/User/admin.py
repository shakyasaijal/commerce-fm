from django.contrib import admin
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from . import models


if settings.HAS_ADDITIONAL_USER_DATA:
    try:
        class UserProfileInline(admin.TabularInline):
            model = models.UserProfile
            extra = 0
    except (Exception, KeyError) as e:
        raise ImproperlyConfigured("User/admin.py:: Multi Vendor is turned on.")


class UserAdmin(admin.ModelAdmin):
    list_display = ['get_full_name', 'email', 'is_verified']
    search_fields = ['get_full_name', 'email', 'date_joined', 'username']
    list_filter = ('groups',)

    if settings.HAS_ADDITIONAL_USER_DATA:
        inlines = [ UserProfileInline, ]


    def save_model(self, request, obj, form, change):
        if 'password' in form.changed_data:
            obj.set_password(request.POST['password'])
        obj.save()

admin.site.register(models.User, UserAdmin)