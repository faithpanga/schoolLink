from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Event
import datetime

@login_required
def create_event(request):
    if request.method == 'POST':
        Event.objects.create(
            creator=request.user,
            title=request.POST['title'],
            description=request.POST['description'],
            date=request.POST['date'],
        )
        return redirect('view_events')
    return render(request, 'events/create_event.html')

@login_required
def view_events(request):
    events = Event.objects.filter(date__gte=datetime.date.today()).order_by('date')
    return render(request, 'events/view_events.html', {'events': events})

