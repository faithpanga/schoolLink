from django.urls import path, include
from . import views

urlpatterns = [
    path('send_message/<int:student_id>/', views.send_message, name='send_message'),
    path('broadcast_announcement/', views.broadcast_announcement, name='broadcast_announcement'),
    path('communication_log/<int:student_id>/', views.student_communication_log, name='student_communication_log'),
]