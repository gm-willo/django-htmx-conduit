from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("article/<slug:slug>-<uuid:uuid>", views.article_detail, name="article_detail")
]
