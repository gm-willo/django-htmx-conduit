from django.urls import path

from .views import Login, Logout, SignUpView

from . import views


urlpatterns = [
    path("login", Login.as_view(), name="login"),
    path("logout", Logout.as_view(), name="logout"),
    path("signup", SignUpView.as_view(), name="signup"),
    path("profile/@<str:username>", views.profile_detail, name="profile_detail"),
    path("settings", views.profile_update, name="settings"),
    path("profile/@<str:username>/follow", views.profile_follow, name="profile_follow"),
    path("profile/@<str:username>/favorites", views.profile_detail, name="profile_favorites"),
]
