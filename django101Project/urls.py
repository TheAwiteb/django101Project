from django.contrib import admin
from django.urls import path, include
from . import views

from django.conf import settings
from django.conf.urls.static import static


# يتم تشغيل هذا الفيو في حال حدوث خطأ 404
handler404 = "django101Project.views.handler404"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="Home"),
    path("settings/", views.Settings.as_view(), name="settings"),
    path("courses/", include("coursesApp.urls")),
    path("about/", views.about, name="About"),
    path("user/<str:username>", views.profile, name="profile"),
    path("registration/", include("registration.urls")),
] + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)  # لعرض وجلب ملفات الميديا
