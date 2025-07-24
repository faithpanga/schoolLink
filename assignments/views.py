from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from students.models import Student
from .forms import AssignmentForm


@login_required
def send_assignment(request, student_id):
    student = get_object_or_404(Student, id=student_id, teacher=request.user)
    if request.method == "POST":
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.teacher = request.user
            assignment.student = student
            assignment.save()
            messages.success(
                request,
                f"Assignment '{assignment.title}' sent to the parent of {student.first_name}.",
            )
            return redirect("teacher_dashboard")
    else:
        form = AssignmentForm()
    return render(
        request, "assignments/send_assignment.html", {"form": form, "student": student}
    )
