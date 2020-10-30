from django.urls import reverse_lazy
from django.conf import settings


all_navigation_routes = [
    {
        'title': 'dashboard',
        'url': reverse_lazy('vendor-home'),
        'superuser': False,
        'icon': 'fa fa-dashboard',
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
        'icon': 'fa fa-users',
        'service': '',
        'group': False,
        'permission': 'auth.view_group',
        'vendorOnly': True,
        'links': [],
    },
    {
        'title': 'users',
        'url': reverse_lazy('vendor-users'),
        'service': '',
        'superuser': False,
        'icon': 'fa fa-user',
        'group': False,
        'permission': 'api.view_user',
        'vendorOnly': False,
        'links': [],
    },
    {
        'group': True,
        'title': 'products',
        'superuser': False,
        'icon': 'fa fa-sitemap',
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
        'title': 'orders',
        'superuser': False,
        'icon': 'fa fa-cart-plus',
        'service': '',
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
    }
]

if settings.MULTI_VENDOR:
    all_navigation_routes += [
        {
            'group': True,
            'title': 'vendor management',
            'superuser': True,
            'icon': 'fa fa-object-group',
            'permission': 'Vendor.view_vendor',
            'service': 'multi-vendor',
            'vendorOnly': False,
            'links': [
                {
                    'title': 'vendors',
                    'url': reverse_lazy('vendor-vendors'),
                    'permission': 'Vendor.view_vendor'
                },
                {
                    'title': 'delivered orders',
                    'url': reverse_lazy('vendor-delivered'),
                    'permission': 'OrderAndDelivery.view_orders'
                },
            ]
        }
    ]


if settings.HAS_OFFER_APP:
    all_navigation_routes += [
        {
            'title': 'special offers',
            'superuser': False,
            'icon': 'fa fa-users',
            'service': '',
            'group': True,
            'permission': '',
            'vendorOnly': False,
            'links': [
                {
                    'title': 'all offers',
                    'url': reverse_lazy('vendor-offers'),
                    'permission': 'Offer.view_offer'
                },
                {
                    'title': 'participate in offers',
                    'url': reverse_lazy('vendor-offers'),
                    'permission': 'Offer.view_offer'
                },
            ]
        }
    ]

all_navigation_routes += [
    {
        'title': 'company information',
        'url': reverse_lazy('vendor-company-info'),
        'superuser': False,
        'icon': 'fa fa-info',
        'service': '',
        'group': False,
        'permission': 'CompanyInformation.view_companyinformation',
        'vendorOnly': False,
        'links': [],
    },
]