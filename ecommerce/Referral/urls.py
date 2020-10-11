from django.urls import path
from . import views

urlpatterns = [
    path('', views.JoinRefer.as_view(), name="vendor-refer-join"),
]
