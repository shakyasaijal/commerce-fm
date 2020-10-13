from rest_framework import routers
from . import views as api_views

router = routers.DefaultRouter()
router.register('get', api_views.ProductInfo, "products-info"),

# Products and comments
router.register('comment', api_views.CommentProduct, "product-comment"),

# Category
router.register('category', api_views.CategoryInfo, "category-info"),
router.register('category/popular', api_views.PopularCategory,
                "category-popular"),
urlpatterns = router.urls
