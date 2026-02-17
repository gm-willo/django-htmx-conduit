from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("article/<slug:slug>-<uuid:uuid>", views.article_detail, name="article_detail"),
    path("editor/", views.article_create, name="article_create"),
    path("editor/<slug:slug>-<uuid:uuid>", views.article_update, name="article_update"),
    path("editor/<slug:slug>-<uuid:uuid>/delete", views.article_delete, name="article_delete"),
]
