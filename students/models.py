from django.db import models
from django.conf import settings


class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="students",
        limit_choices_to={"role": "TEACHER"},
    )
    parent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="children",
        limit_choices_to={"role": "PARENT"},
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
