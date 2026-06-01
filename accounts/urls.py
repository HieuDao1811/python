from django.urls import path
from .views import RoleBasedLoginView, register, logout_view

urlpatterns = [
    path("login/", RoleBasedLoginView.as_view(), name="login"),
    path("register/", register, name="register"),
    path("logout/", logout_view, name="logout"),
]