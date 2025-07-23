from django.db import models
from schoolLink.settings import AUTH_USER_MODEL

class Student(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    parent = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='children', limit_choices_to={'role': 'PA'})
    teacher = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='students', limit_choices_to={'role': 'TE'})

    def __str__(self):
        return f"{self.first_name} {self.last_name}"