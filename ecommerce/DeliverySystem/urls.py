from django.urls import path
from django.conf import settings
from . import views


urlpatterns = [
    path('', views.Index.as_view(), name="delivery-index"),
    path('login', views.LoginView.as_view(), name="delivery-login"),

    # All taken and untaken orders
    path('orders', views.OrderView.as_view(), name="delivery-order"),

    # Orders Details
    path('orders/details/<int:id>', views.OrderDetail.as_view(), name="delivery-order-details"),

    # Only my delivery orders
    path('my-delivery', views.MyDelivery.as_view(), name="delivery-my-delivery"),

    # All untaken and unassigned orders
    path('pending-delivery', views.PendingDelivery.as_view(), name="delivery-pending"),

    # To take a delivery responsibility
    path('take-delivery', views.TakeDelivery.as_view(), name="delivery-take-delivery"),

    path('cancelled-order', views.CancelDelivery.as_view(), name="delivery-cancelled")
]
