from django.urls import reverse_lazy
from django.contrib.auth.models import Permission
from django.conf import settings

from . import helper

template_version = 'v1'

try:
    template_version = settings.TEMPLATE_VERSION
except Exception:
    pass

if template_version == "v1":
    from .allRoutes.v1 import routes
elif template_version == "v2":
    from .allRoutes.v2 import routes

admin_navigation_routes = [route for route in routes.all_navigation_routes]
vendor_navigation_routes = [route for route in routes.all_navigation_routes if route['superuser']==False]

