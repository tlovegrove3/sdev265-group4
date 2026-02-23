from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import EventForm


@login_required
def event_create(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.creator = request.user
            form.save()
            return redirect("events:event_list")  # temporary until detail view exists
    else:
        form = EventForm()

    return render(request, "events/event_create.html", {"form": form})


def event_list(request):
    return render(request, "events/event_list.html")
