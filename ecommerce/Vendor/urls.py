from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.VendorsList.as_view(), name="vendor-vendors"),
    path('join', views.JoinAsVendor.as_view(), name="vendor-join"),
    path('register', views.RegisterAsVendor.as_view(), name="vendor-join-register"),
    path('vr-delete', views.DeleteVendorRequest.as_view(), name="vendor-vr-delete"),
    path('vr-edit', views.EditVendorRequest.as_view(), name="vendor-vr-edit"),
    path('resend-email/<int:id>', views.ResendRegistrationEmail.as_view(), name="vendor-resend-email")
]
