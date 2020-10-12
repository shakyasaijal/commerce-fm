from rest_framework import routers
from django.urls import include, path, re_path
from . import views as api_views

router = routers.DefaultRouter()
router.register('wishlist', api_views.Wishlist, "cart-wishlist"),
router.register('items', api_views.CartItems, "cart-items"),
router.register('wishlist-to-cart', api_views.WishlistToCart, "cart-wishlist-to-cart"),
router.register('add-to-cart', api_views.AddToCart, "cart-add")
urlpatterns = [
]

urlpatterns += router.urls
