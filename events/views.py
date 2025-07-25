from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from events.forms import EventForm
from .models import Event
import datetime


@login_required
def create_event(request):
    if request.user.role != "TEACHER":
        return redirect("home")

    if request.method == "POST":
        form = EventForm(request.POST)  # Bind the POST data to the form
        if form.is_valid():
            # Create an event instance but don't save to DB yet
            event = form.save(commit=False)
            event.creator = request.user  # Set the creator manually
            event.save()  # Now save the complete object

            messages.success(request, f"Event '{event.title}' has been created.")
            return redirect("view_events")
    else:
        form = EventForm()  # Create an empty form for a GET request

    return render(request, "events/create_event.html", {"form": form})


@login_required
def view_events(request):
    events = Event.objects.filter(date__gte=datetime.date.today()).order_by("date")
    return render(request, "events/view_events.html", {"events": events})
