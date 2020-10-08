from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('information', views.CompanyInformation.as_view(), name="vendor-company-info"),

    # Contact
    path('create-contact', views.CreateContact.as_view(), name="vendor-create-contact"),
    path('delete-contact/<int:id>', views.DeleteContact.as_view(), name="vendor-delete-contact"),
    path('edit-contact/<int:id>', views.EditContact.as_view(), name="vendor-edit-contact"),

    # Basic
    path('edit-info', views.EditInfo.as_view(), name="vendor-edit-info"),

    # Social Media
    path('edit-social-info', views.EditSocialInfo.as_view(), name="vendor-edit-social-info"),

]
