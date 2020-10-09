from rest_framework import routers
from django.urls import include, path, re_path
from . import views as api_views
from rest_framework_simplejwt import views as jwt_views

router = routers.DefaultRouter()
router.register('featured-category',
                api_views.FeaturedCategory, "featured-category"),
router.register('featured-products',
                api_views.FeaturedProducts, "featured-products"),
router.register('offers', api_views.Offers, "offers"),
router.register('just-for-you', api_views.JustForYou, "just-for-you"),
router.register('ok', api_views.Ok, "ok"),
router.register('recent-arrivals', api_views.RecentArrivals,
                "recent-arrivals"),

urlpatterns = [
    path("activate/<token>",api_views.activate, name="activate"),
    path('products/', include(('Products.Api.urls',
                               'Product'), namespace='products_detail')),
    path('carts/', include(('CartSystem.Api.urls', 'Carts'),
                           namespace="carts_and_wishlists")),
    path('company/', include(('CompanyInformation.Api.urls', 'Company Info'), namespace='company_info')),
    path('user/', include(('User.Api.urls', 'User Related API'), namespace='user_api')),
    path('referal/', include(('Referral.Api.urls', 'Refer and Reward API'), namespace='refer_api')),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += router.urls
