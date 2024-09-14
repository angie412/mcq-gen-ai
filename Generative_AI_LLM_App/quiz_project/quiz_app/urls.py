from django.contrib import admin
from django.urls import path
from quiz_app import views
from .views import TestListView, download
urlpatterns = [
    path("", views.home, name = "home"),
    path("history/", TestListView.as_view(), name = "test_list"),
    path("download/<int:test_id>", download, name= "test_download")

]
