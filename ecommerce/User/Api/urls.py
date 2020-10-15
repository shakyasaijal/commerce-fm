from rest_framework import routers
from . import views as api_views

router = routers.DefaultRouter()

# Auth and Profile
router.register("complete-profile", api_views.CompleteProfile,
                "user-complete-profile")
router.register("register", api_views.RegisterUser, "user-register"),
router.register("login", api_views.LoginUser, "user-login"),
router.register("logout", api_views.LogoutUser, "user-logout"),
router.register("google-login", api_views.GoogleLogin, "user-google-login"),
router.register("facebook-login", api_views.FacebookLogin,
                "user-facebook-login"),

# Password
router.register("change-password", api_views.ChangePassword,
                "user-change-password"),

router.register("marketing", api_views.Marketing, "user-marketing"),
router.register("interests", api_views.Interest, "user-interest"),
router.register("update-interests", api_views.UpdateInterest,
                "user-update-interest"),

urlpatterns = router.urls
