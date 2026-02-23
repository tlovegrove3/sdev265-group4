from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from .forms import EventForm
from .models import Event


@login_required
def event_create(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.creator = request.user
            form.save()
            return redirect("events:event_detail", pk=event.pk)
    else:
        form = EventForm()

    return render(request, "events/event_create.html", {"form": form})


def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    is_creator = request.user == event.creator
    return render(
        request,
        "events/event_detail.html",
        {
            "event": event,
            "is_creator": is_creator,
        },
    )


@login_required
def event_edit(request, pk):
    event = get_object_or_404(Event, pk=pk)

    if request.user != event.creator:
        return HttpResponseForbidden("You can only edit your own events.")

    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect("events:event_detail", pk=event.pk)
    else:
        form = EventForm(instance=event)

    return render(request, "events/event_edit.html", {"form": form, "event": event})


def event_list(request):
    return render(request, "events/event_list.html")
