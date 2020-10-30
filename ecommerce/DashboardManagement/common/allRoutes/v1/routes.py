from django.urls import reverse_lazy

all_navigation_routes = [
    {
        'title': 'dashboard',
        'url': reverse_lazy('vendor-home'),
        'superuser': False,
        'icon': 'fas fa-fw fa-tachometer-alt',
        'service': '',
        'group': False,
        'permission': '',
        'vendorOnly': False,
        'links': [],
    },
    {
        'title': 'groups and permissions',
        'url': reverse_lazy('vendor-groups'),
        'superuser': False,
        'icon': 'fas fa-fw fa-users',
        'service': '',
        'group': False,
        'permission': 'auth.view_group',
        'vendorOnly': True,
        'links': [],
    },
    {
        'title': 'users',
        'url': reverse_lazy('vendor-users'),
        'superuser': False,
        'icon': 'fas fa-fw fa-user',
        'service': '',
        'group': False,
        'permission': 'api.view_user',
        'vendorOnly': False,
        'links': [],
    },
    {
        'group': True,
        'title': 'products',
        'superuser': False,
        'icon': 'fas fa-fw fa-cog',
        'service': '',
        'permission': '',
        'vendorOnly': False,
        'links': [
            {
                'title': 'category',
                'url': reverse_lazy('category'),
                'permission': 'Products.view_category'
            },
            {
                'title': 'products',
                'url': reverse_lazy('products'),
                'permission': 'Products.view_product'
            },
        ]
    },
    {
        'group': True,
        'service': '',
        'title': 'orders',
        'superuser': False,
        'icon': 'fas fa-fw fa-cog',
        'permission': '',
        'vendorOnly': False,
        'links': [
            {
                'title': 'pending/new orders',
                'url': reverse_lazy('vendor-orders'),
                'permission': 'OrderAndDelivery.view_orders'
            },
            {
                'title': 'delivered orders',
                'url': reverse_lazy('vendor-delivered'),
                'permission': 'OrderAndDelivery.view_orders'
            },
        ]
    },
]
