from django.db import models
from django.conf import settings
from students.models import Student


class Message(models.Model):
    class Source(models.TextChoices):
        APP = "APP", "Application"
        SMS = "SMS", "SMS"

    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="messages"
    )
    subject = models.CharField(max_length=255)
    body = models.TextField()
    is_broadcast = models.BooleanField(default=False)
    source = models.CharField(max_length=10, choices=Source.choices, default=Source.APP)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject
