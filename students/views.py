from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .forms import AddStudentForm
from .models import Student
from accounts.models import User
from events.models import Event
from accounts.views import send_account_setup_email
import datetime
import logging

logger = logging.getLogger(__name__)


@login_required
def teacher_dashboard(request):
    if request.user.role != "TEACHER":
        return redirect("home")

    query = request.GET.get("q", "")
    students = Student.objects.filter(teacher=request.user)
    if query:
        students = students.filter(
            Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
            | Q(parent__first_name__icontains=query)
            | Q(parent__last_name__icontains=query)
        )

    return render(
        request,
        "students/teacher_dashboard.html",
        {"students": students, "query": query},
    )


@login_required
def parent_dashboard(request):
    if request.user.role != "PARENT":
        return redirect("home")
    children = Student.objects.filter(parent=request.user)
    upcoming_events = Event.objects.filter(date__gte=datetime.date.today()).order_by(
        "date"
    )[:3]
    return render(
        request,
        "students/parent_dashboard.html",
        {"children": children, "upcoming_events": upcoming_events},
    )


@login_required
def add_student(request):
    if request.user.role != "TEACHER":
        return redirect("home")
    if request.method == "POST":
        form = AddStudentForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            parent = None
            try:
                parent = User.objects.get(email=data["parent_email"])
            except User.DoesNotExist:
                parent = User.objects.create(
                    email=data["parent_email"],
                    first_name=data["parent_first_name"],
                    last_name=data["parent_last_name"],
                    phone_number=data["parent_phone"],
                    role="PARENT",
                )
                parent.set_unusable_password()
                parent.save()
                try:
                    send_account_setup_email(parent, request)
                    messages.success(
                        request,
                        f"New parent account for {parent.email} created. They will receive a setup email.",
                    )
                except Exception as e:
                    logger.error(f"Failed to send setup email to {parent.email}: {e}")
                    messages.warning(
                        request,
                        f"Parent account for {parent.email} created, but the setup email failed to send. Please check logs.",
                    )

            Student.objects.create(
                first_name=data["student_first_name"],
                last_name=data["student_last_name"],
                teacher=request.user,
                parent=parent,
            )
            messages.success(
                request, f"Student '{data['student_first_name']}' has been added."
            )
            return redirect("teacher_dashboard")
    else:
        form = AddStudentForm()
    return render(request, "students/add_student.html", {"form": form})
