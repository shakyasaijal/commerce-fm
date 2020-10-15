from django.urls import path
from django.conf import settings
from . import views


urlpatterns = [
    path('', views.Index.as_view(), name="delivery-index"),
    path('login', views.LoginView.as_view(), name="delivery-login"),
]