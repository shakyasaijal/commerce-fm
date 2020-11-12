from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.OfferView.as_view(), name="vendor-offers"),
    path('add', views.AddOfferView.as_view(), name="vendor-offers-add"),
    path('delete', views.DeleteOffers.as_view(), name="vendor-offers-delete"),
    path('edit/<int:id>', views.EditOffers.as_view(), name="vendor-offers-edit"),
    path('add-product/<int:id>', views.ListProductToAddInOffer.as_view(),
            name='add-product-to-offer'),
]