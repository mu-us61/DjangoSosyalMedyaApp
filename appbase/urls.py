from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register", views.myregister, name="register"),
    path("login", views.mylogin, name="login"),
    path("logout", views.mylogout, name="logout"),
    path("profile", views.profile, name="profile"),
    path("postdetail/<uuid:id>/", views.postdetail, name="postdetail"),
    path("createpost", views.createpost, name="createpost"),
    path("myposts", views.myposts, name="myposts"),
    path("user/<str:username>/", views.user, name="user"),
    path("post/<uuid:post_id>/like/", views.toggle_like, name="toggle_like"),
]
