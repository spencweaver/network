
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    #API Routes
    path("posts", views.compose, name="compose"),
    # path("posts/<int:post_id>", views.post, name="post"),
    path("post_view", views.post_view, name="post_view"),
    path("like/<int:post_id>", views.like, name="like"),
]
