from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("Courses-list", views.coursesList, name="courses-list"),
    path("About", views.about, name="about"),
]
