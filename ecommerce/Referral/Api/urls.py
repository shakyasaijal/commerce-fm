from rest_framework import routers
from django.urls import path
from . import views as api_views

router = routers.DefaultRouter()
router.register("join", api_views.JoinReferral, "refer-join")

urlpatterns = router.urls
