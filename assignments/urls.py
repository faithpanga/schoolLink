from django.urls import path
from . import views

urlpatterns = [
    path("send/<int:student_id>/", views.send_assignment, name="send_assignment"),
]
