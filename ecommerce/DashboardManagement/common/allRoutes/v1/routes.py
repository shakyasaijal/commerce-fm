from django.urls import reverse_lazy

all_navigation_routes = [
    {
        'title': 'dashboard',
        'url': reverse_lazy('vendor-home'),
        'superuser': False,
        'icon': 'fas fa-fw fa-tachometer-alt',
        'service': '',
        'group': False,
        'permission': ''
    },
    {
        'title': 'groups and permissions',
        'url': reverse_lazy('vendor-groups'),
        'superuser': False,
        'icon': 'fas fa-fw fa-users',
        'service': '',
        'group': False,
        'permission': 'auth.view_group'
    },
    {
        'title': 'users',
        'url': reverse_lazy('vendor-users'),
        'superuser': False,
        'icon': 'fas fa-fw fa-user',
        'service': '',
        'group': False,
        'permission': 'api.view_user'
    },
    {
        'group': True,
        'title': 'products',
        'superuser': False,
        'icon': 'fas fa-fw fa-cog',
        'service': '',
        'permission': '',
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
