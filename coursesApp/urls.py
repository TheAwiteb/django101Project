from django.urls import path
from . import views

urlpatterns = [
    path("", views.coursesList, name="courses-list"),
]
