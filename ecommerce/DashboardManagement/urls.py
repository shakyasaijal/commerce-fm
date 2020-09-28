from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name="vendor-home"),

    # Authentication
    path('login', views.LoginView.as_view(), name="vendor-login"),
    path('logout', views.LogoutView.as_view(), name="vendor-logout"),

    # Groups and Permissions
    path('groups', views.GroupView.as_view(), name="vendor-groups"),
    path('group/<int:id>', views.GroupDetailView.as_view(), name="vendor-group-detail"),
    path('create-group', views.CreateGroup.as_view(), name="vendor-create-group"),
    path('delete-group/<int:id>', views.DeleteGroup.as_view(), name="vendor-delete-group"),

    # Users
    path('users', views.UsersView.as_view(), name="vendor-users"),
    path('create-users', views.CreateUser.as_view(), name="vendor-create-users"),
    path('delete-user/<int:id>', views.DeleteUser.as_view(), name="vendor-delete-users"),
    path('edit-user/<int:id>', views.EditUser.as_view(), name="vendor-edit-users"),
]
