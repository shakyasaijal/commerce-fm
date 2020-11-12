from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name="vendor-home"),

    # Authentication
    path('login', views.LoginView.as_view(), name="vendor-login"),
    path('logout', views.LogoutView.as_view(), name="vendor-logout"),
    path('change-password', views.ChangePassword.as_view(), name="change-password"),


    # Groups and Permissions
    path('groups', views.GroupView.as_view(), name="vendor-groups"),
    path('group/<int:id>', views.GroupDetailView.as_view(),
         name="vendor-group-detail"),
    path('create-group', views.CreateGroup.as_view(), name="vendor-create-group"),
    path('delete-group/<int:id>', views.DeleteGroup.as_view(),
         name="vendor-delete-group"),

    # Users
    path('users', views.UsersView.as_view(), name="vendor-users"),
    path('create-users', views.CreateUser.as_view(), name="vendor-create-users"),
    path('delete-user/<int:id>', views.DeleteUser.as_view(),
         name="vendor-delete-users"),
    path('edit-user/<int:id>', views.EditUser.as_view(), name="vendor-edit-users"),

    path('profile', views.Profile.as_view(), name="profile"),

    # Products and Categories
    path('products', views.ProductList.as_view(), name="products"),
    path('products/add', views.Product.as_view(), name="product-add"),
    path('products/delete', views.ProductDelete.as_view(),
         name="vendor-product-delete"),
    path('products/edit/<int:id>', views.ProductEdit.as_view(),
         name="vendor-product-edit"),
    path('category', views.CategoryList.as_view(), name="category"),
    path('category/delete/<id>', views.CategoryDelete.as_view(),
         name="category-delete"),
    path('category/add', views.Category.as_view(), name="category-add"),
    path('category/edit/<id>', views.CategoryEdit.as_view(), name="category-edit"),
    path('category/request', views.RequestNewCategory.as_view(), name="category-request"),
    path('category/request/delete', views.RequestNewCategoryDelete.as_view(), name="category-request-delete"),

    # Orders
    path('orders/', include('OrderAndDelivery.urls')),

    # Vendor
    path('vendors/', include('Vendor.urls')),

    # Offers
    path('offers/', include('Offer.urls')),

    # Company Information
    path('company/', include('CompanyInformation.urls')),

    # Refer
    path('refer/', include('Referral.urls')),

    path('comments', views.ProductComment.as_view(), name="comments"),
    path('comments/<id>',
        views.CommentDetails.as_view(), name="comment-detail"),
    path('comments/delete/<id>', views.CommentDelete.as_view(), name="comment-delete"),
    path('comments/approve/<id>', views.CommentApprove.as_view(), name="comment-approve"),
    path('comments/edit/<int:id>', views.CommentEdit.as_view(), name="comment-edit"),
    path('offers/', include('Offer.urls'))
]
