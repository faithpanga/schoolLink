from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    class Role(models.TextChoices):
        PARENT = 'PA', 'Parent'
        TEACHER = 'TE', 'Teacher'
    role = models.CharField(max_length=2, choices=Role.choices, default=Role.PARENT)

    def __str__(self):
        return self.username