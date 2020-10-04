from rest_framework import routers
from django.urls import include, path, re_path
from . import views as api_views

router = routers.DefaultRouter()
router.register('get', api_views.ProductInfo, "products-info"),
router.register('category', api_views.CategoryInfo, "category-info"),
urlpatterns = [
]

urlpatterns += router.urls
