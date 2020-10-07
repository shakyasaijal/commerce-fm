from rest_framework import routers
from django.urls import include, path, re_path
from . import views as api_views


router = routers.DefaultRouter()
router.register('featured-category',
                api_views.FeaturedCategory, "featured-category"),
router.register('featured-products',
                api_views.FeaturedProducts, "featured-products"),
router.register('offers', api_views.Offers, "offers"),
router.register('just-for-you', api_views.JustForYou, "just-for-you"),
router.register('recent-arrivals', api_views.RecentArrivals,
                "recent-arrivals"),

urlpatterns = [
    path('products/', include(('Products.Api.urls',
                               'Product'), namespace='products_detail')),
    path('carts/', include(('CartSystem.Api.urls', 'Carts'),
         namespace="carts_and_wishlists"))
]

urlpatterns += router.urls
