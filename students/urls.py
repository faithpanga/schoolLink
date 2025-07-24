from django.urls import path
from . import views

urlpatterns = [
    path("teacher/", views.teacher_dashboard, name="teacher_dashboard"),
    path("parent/", views.parent_dashboard, name="parent_dashboard"),
    path("add/", views.add_student, name="add_student"),
]
