from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.article, name="article"),
    path("search/", views.search, name="search"),
    path("new/", views.newEntry, name="newEntry"),
    path("edit/<str:title>", views.editEntry, name="editEntry"),
    path("random/", views.randomArticle, name="random")
]
