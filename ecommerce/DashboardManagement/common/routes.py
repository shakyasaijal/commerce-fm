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

def get_routes(user):
    if settings.MULTI_VENDOR:
        if user.is_superuser:
            return admin_navigation_routes
        elif helper.is_vendor_admin(user):
            return vendor_navigation_routes
        else:
            return routes_by_permissions(user)
    else:
        if user.is_superuser:
            return admin_navigation_routes
        else:
            return routes_by_permissions(user)


def routes_by_permissions(user):
    users_all_pemissions = Permission.objects.filter(
        group__user=user).order_by('-content_type')
    routes = []
    try:
        for route in all_navigation_routes:
            if route['service'] == 'multi-vendor' and settings.MULTI_VENDOR or routes['service'] == '':
                try:
                    possible_links = []
                    for data in route["links"]:
                        if data["permission"]:
                            if user.has_perm(data["permission"]):
                                possible_links.append(data)
                    if possible_links:
                        route['links'] = possible_links
                        routes.append(route)
                except Exception as e:
                    if route["permission"]:
                        if user.has_perm(route["permission"]):
                            routes.append(route)
                    else:
                        routes.append(route)
        return routes
    except Exception as e:
        print(e)
        return routes


def get_formatted_routes(routes, active_page):
    formatted_routes = []
    for route in routes:
        route['active'] = False
        if route['title'] == active_page:
            route['active'] = True
        formatted_routes.append(route)
    return formatted_routes
