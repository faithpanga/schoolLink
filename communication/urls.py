from django.urls import path
from . import views

urlpatterns = [
    path("broadcast/", views.broadcast_announcement, name="broadcast_announcement"),
    path("log/<int:student_id>/", views.communication_log, name="communication_log"),
]
