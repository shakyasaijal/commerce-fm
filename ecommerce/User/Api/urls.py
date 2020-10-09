from rest_framework import routers
from . import views as api_views

router = routers.DefaultRouter()
router.register("register", api_views.RegisterUser, "user-register"),
router.register("login", api_views.LoginUser, "user-login"),
router.register("logout", api_views.LogoutUser, "user-logout"),
router.register("google-login", api_views.GoogleLogin, "user-google-login"),
router.register("facebook-login", api_views.FacebookLogin, "user-facebook-login"),
urlpatterns = router.urls