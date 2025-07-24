from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import home_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home_view, name="home"),
    path("accounts/", include("accounts.urls")),
    path("students/", include("students.urls")),
    path("communication/", include("communication.urls")),
    path("events/", include("events.urls")),
    path("assignments/", include("assignments.urls")),
    path("sms/", include("sms_handler.urls")),
    # path("tailwind/", include("django-tailwind.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
