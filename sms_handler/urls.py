from django.urls import path
from . import views

urlpatterns = [
    path("webhook/", views.sms_webhook, name="sms_webhook"),
]
