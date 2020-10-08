from rest_framework import routers
from . import views as api_views

router = routers.DefaultRouter()
router.register("register", api_views.RegisterUser, "user-register")
urlpatterns = router.urls
