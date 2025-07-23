from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView # <-- Import this

urlpatterns = [
    # Add this line: It makes the root URL redirect to the login page
    path('', RedirectView.as_view(url='/accounts/login/', permanent=False), name='index'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('dashboard/', include('students.urls')),
    path('communication/', include('communication.urls')),
    path('events/', include('events.urls')),
]