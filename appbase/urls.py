from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register", views.myregister, name="register"),
    path("login", views.mylogin, name="login"),
]
