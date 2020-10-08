from rest_framework import routers
from django.urls import include, path, re_path
from . import views as api_views

router = routers.DefaultRouter()
router.register('info', api_views.CompanyInfo, "company-information"),
urlpatterns = router.urls