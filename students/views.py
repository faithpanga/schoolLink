from django.contrib.auth.decorators import login_required
from accounts.decorators import role_required
from django.db.models import Q
from django.shortcuts import render
from .models import Student


@login_required
def teacher_dashboard(request):
    students = Student.objects.filter(teacher=request.user)
    context = {"students": students}
    return render(request, "students/teacher_dashboard.html", context)


@login_required
@role_required("PARENT")
def parent_dashboard(request):
    """
    Displays updates for children linked to the logged-in parent.
    """
    children = request.user.children.all()

    for student in children:
        # Get all private messages for the student PLUS all broadcast messages from their teacher
        student.messages = (
            Message.objects.filter(
                Q(student=student, is_broadcast=False)
                | Q(sender=student.teacher, is_broadcast=True)
            )
            .distinct()
            .order_by("-timestamp")[:5]
        )  # Get latest 5

    context = {"children": children}
    return render(request, "students/parent_dashboard.html", context)
