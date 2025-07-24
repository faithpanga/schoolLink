from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.create_event, name="create_event"),
    path("", views.view_events, name="view_events"),
]
