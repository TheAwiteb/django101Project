"""django101Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views

from django.conf import settings
from django.conf.urls.static import static


handler404 = "django101Project.views.handler404"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="Home"),
    path("settings/", views.Settings.as_view(), name="settings"),
    path("courses/", include("coursesApp.urls")),
    path("about/", views.about, name="About"),
    path("user/<str:username>", views.profile, name="profile"),
    path("registration/", include("registration.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
