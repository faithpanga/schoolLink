from django.db import models
from schoolLink.settings import AUTH_USER_MODEL

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    creator = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'role': 'TE'})

    def __str__(self):
        return self.title