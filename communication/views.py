# communication/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from students.models import Student
from .models import Message
from .forms import BroadcastForm, MessageForm  # Import both forms
from .sms_utils import send_sms


@login_required
def broadcast_announcement(request):
    """
    Handles sending a broadcast message to all parents.
    This view now correctly uses the BroadcastForm for validation.
    """
    if request.user.role != "TEACHER":
        messages.error(request, "You do not have permission to perform this action.")
        return redirect("home")

    if request.method == "POST":
        form = BroadcastForm(request.POST)
        if form.is_valid():
            # All the logic now goes INSIDE the is_valid() block.
            subject = form.cleaned_data["subject"]
            body = form.cleaned_data["body"]
            send_sms_alert = form.cleaned_data["send_sms"]

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
                if send_sms_alert and student.parent.phone_number:
                    sms_body = f"School Announcement: {subject}. Please log in to your SchoolLink dashboard for details."
                    if send_sms(student.parent.phone_number, sms_body):
                        sms_sent_count += 1

            if send_sms_alert:
                messages.success(
                    request,
                    f"Broadcast sent successfully. {sms_sent_count} SMS alerts were delivered.",
                )
            else:
                messages.success(request, "Broadcast sent successfully.")

            # A successful POST should always end with a redirect.
            return redirect("teacher_dashboard")
        # If the form is NOT valid, the view will fall through to the final render,
        # and the `form` object will now contain the errors to display.
    else:
        # For a GET request, create an empty form.
        form = BroadcastForm()

    # This line is reached on a GET request or if the POST form was invalid.
    return render(request, "communication/broadcast.html", {"form": form})


@login_required
def communication_log(request, student_id):
    """
    Displays the conversation history for a student and handles replies.
    This view is now upgraded to use the MessageForm.
    """
    student = get_object_or_404(Student, id=student_id)
    if request.user != student.teacher and request.user != student.parent:
        messages.error(request, "You do not have permission to view this page.")
        return redirect("home")

    if request.method == "POST":
        message_form = MessageForm(request.POST)  # Use the new MessageForm
        if message_form.is_valid():
            body = message_form.cleaned_data["body"]
            send_sms_alert = message_form.cleaned_data["send_sms"]

            Message.objects.create(
                sender=request.user,
                student=student,
                subject=f"Reply in conversation for {student.first_name}",
                body=body,
            )
            # Your SMS notification logic can be simplified slightly
            if send_sms_alert:
                if request.user.role == "TEACHER" and student.parent.phone_number:
                    sms_body = f"New message from your teacher regarding {student.first_name}. Please log in to reply."
                    send_sms(student.parent.phone_number, sms_body)
                elif request.user.role == "PARENT" and student.teacher.phone_number:
                    sms_body = f"New message from {student.parent.first_name} (parent of {student.first_name}). Please log in to view."
                    send_sms(student.teacher.phone_number, sms_body)

            messages.success(request, "Message sent.")
        else:
            messages.error(request, "Cannot send an empty message.")

        # Always redirect after a POST to prevent double-submissions
        return redirect("communication_log", student_id=student.id)

    # For a GET request, create empty forms
    communications = student.messages.all().order_by("timestamp")
    message_form = MessageForm()

    return render(
        request,
        "communication/communication_log.html",
        {
            "student": student,
            "communications": communications,
            "message_form": message_form,  # Pass the form to the template
        },
    )
