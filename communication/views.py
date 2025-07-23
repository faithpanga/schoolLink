from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Message
from students.models import Student

@login_required
def send_message(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        Message.objects.create(
            sender=request.user,
            recipient=request.POST.get('recipient'),
            student=student,
            subject=request.POST.get('subject'),
            body=request.POST.get('body'),
        )
        return redirect('student_communication_log', student_id=student.id)
    return render(request, 'communication/send_message.html', {'student': student})

@login_required
def broadcast_announcement(request):
    if request.method == 'POST':
        Message.objects.create(
            sender=request.user,
            is_broadcast=True,
            subject=request.POST.get('subject'),
            body=request.POST.get('body'),
        )
        return redirect('teacher_dashboard')
    return render(request, 'communication/broadcast.html')

@login_required
def student_communication_log(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    messages = Message.objects.filter(student=student).order_by('-timestamp')
    return render(request, 'communication/communication_log.html', {'student': student, 'messages': messages})