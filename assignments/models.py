from django.db import models
from django.conf import settings
from students.models import Student


def assignment_upload_path(instance, filename):
    # Organizes files by teacher and student for clarity
    return f"assignments/teacher_{instance.teacher.id}/student_{instance.student.id}/{filename}"


class Assignment(models.Model):
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="assignments"
    )
    title = models.CharField(max_length=255)
    notes = models.TextField(blank=True, null=True)
    attachment = models.FileField(upload_to=assignment_upload_path)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
