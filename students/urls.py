from django.urls import path, include
from . import views

urlpatterns = [
    path('dashboard/teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('dashboard/parent/', views.parent_dashboard, name='parent_dashboard'),
]