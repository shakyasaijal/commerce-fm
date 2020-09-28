from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.OrderView.as_view(), name="vendor-orders"),
    path('delivered', views.DeliveredView.as_view(), name="vendor-delivered"),
]
