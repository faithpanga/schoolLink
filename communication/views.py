from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from students.models import Student
from .models import Message
from .sms_utils import send_sms


@login_required
def broadcast_announcement(request):
    if request.user.role != "TEACHER":
        return redirect("home")
    if request.method == "POST":
        subject = request.POST.get("subject")
        body = request.POST.get("body")
        send_sms_alert = request.POST.get("send_sms") == "on"

        if not subject or not body:
            messages.error(request, "Subject and body are required for a broadcast.")
            return render(request, "communication/broadcast.html")

        student_list = Student.objects.filter(teacher=request.user)
        sms_sent_count = 0

        for student in student_list:
            Message.objects.create(
                sender=request.user,
                student=student,
                subject=subject,
                body=body,
                is_broadcast=True,
            )
            # THE FIX: Only send SMS if the box was checked AND the parent has a number
            if send_sms_alert and student.parent.phone_number:
                sms_body = f"School Announcement: {subject}. Please log in to your SchoolLink dashboard for details."
                if send_sms(student.parent.phone_number, sms_body):
                    sms_sent_count += 1

        # Give the teacher useful feedback
        if send_sms_alert:
            messages.success(
                request,
                f"Broadcast sent to all parents. {sms_sent_count} SMS alerts were sent.",
            )
        else:
            messages.success(
                request, "Broadcast sent to all parents. No SMS alerts were sent."
            )

        return redirect("teacher_dashboard")

    return render(request, "communication/broadcast.html")


@login_required
def communication_log(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.user != student.teacher and request.user != student.parent:
        messages.error(request, "You do not have permission to view this page.")
        return redirect("home")

    if request.method == "POST":
        body = request.POST.get("body")
        # Check if the SMS box was ticked (only teachers will see this)
        send_sms_alert = request.POST.get("send_sms") == "on"
        if not body:
            messages.error(request, "Cannot send an empty message.")
        else:
            Message.objects.create(
                sender=request.user,
                student=student,
                subject=f"Reply in conversation for {student.first_name}",
                body=body,
            )
            # Notify the other party
            if (
                request.user.role == "TEACHER"
                and student.parent.phone_number
                and send_sms_alert
            ):
                sms_body = f"New message from your teacher regarding {student.first_name}. Please log in to reply."
                send_sms(student.parent.phone_number, sms_body)
            elif request.user.role == "PARENT" and student.teacher.phone_number:
                sms_body = f"New message from {student.parent.first_name} (parent of {student.first_name}). Please log in to view."
                send_sms(student.teacher.phone_number, sms_body)
            messages.success(request, "Message sent.")
        return redirect("communication_log", student_id=student.id)

    communications = student.messages.all().order_by("timestamp")
    return render(
        request,
        "communication/communication_log.html",
        {"student": student, "communications": communications},
    )
