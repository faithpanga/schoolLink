from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Event
import datetime


@login_required
def create_event(request):
    if request.user.role != "TEACHER":
        return redirect("home")
    if request.method == "POST":
        Event.objects.create(
            creator=request.user,
            title=request.POST["title"],
            description=request.POST["description"],
            date=request.POST["date"],
        )
        messages.success(request, f"Event '{request.POST['title']}' has been created.")
        return redirect("view_events")
    return render(request, "events/create_event.html")


@login_required
def view_events(request):
    events = Event.objects.filter(date__gte=datetime.date.today()).order_by("date")
    return render(request, "events/view_events.html", {"events": events})
