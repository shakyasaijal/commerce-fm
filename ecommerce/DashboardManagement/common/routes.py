from django.urls import reverse_lazy
from django.contrib.auth.models import Permission
from django.conf import settings

from . import helper

all_navigation_routes = [
    {
        'title': 'dashboard',
        'url': reverse_lazy('vendor-home'),
        'admin': True,
        'icon': 'fas fa-fw fa-tachometer-alt',
        'group': False,
        'permission': ''
    },
    {
        'title': 'groups and permissions',
        'url': reverse_lazy('vendor-groups'),
        'admin': True,
        'icon': 'fas fa-fw fa-users',
        'group': False,
        'permission': 'auth.view_group'
    },
    {
        'title': 'users',
        'url': reverse_lazy('vendor-users'),
        'admin': True,
        'icon': 'fas fa-fw fa-user',
        'group': False,
        'permission': 'api.view_user'
    },
]

admin_navigation_routes = [route for route in all_navigation_routes]


def get_routes(user):
    if settings.MULTI_VENDOR:
        if helper.is_vendor_admin(user):
            return admin_navigation_routes
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
            try:
                links = route['links']
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
