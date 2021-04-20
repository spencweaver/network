
from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("follow/<int:user_id>", views.follow, name="follow"),
    path("post/<int:user_id>", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    #API Routes
    path("posts", views.compose, name="compose"),
    path("edit/<int:post_id>", views.edit, name="edit"),
    path("post_view", views.post_view, name="post_view"),
    path("like/<int:post_id>", views.like, name="like"),
    
]
