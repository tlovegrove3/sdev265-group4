from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import EventForm
from .models import RSVP, Event


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

    attendee_count = event.rsvps.count()

    attendee_list = None
    if is_creator:
        attendee_list = event.rsvps.select_related("user").all()

    has_rsvped = False
    if request.user.is_authenticated:
        has_rsvped = event.rsvps.filter(user=request.user).exists()

    return render(
        request,
        "events/event_detail.html",
        {
            "event": event,
            "is_creator": is_creator,
            "attendee_count": attendee_count,
            "attendee_list": attendee_list,
            "has_rsvped": has_rsvped,
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

    if event.status == Event.Status.CANCELLED:
        return HttpResponseForbidden("Cancelled events cannot be edited.")

    else:
        form = EventForm(instance=event)

    return render(request, "events/event_edit.html", {"form": form, "event": event})


@login_required
@require_POST
def event_cancel(request, pk):
    event = get_object_or_404(Event, pk=pk)

    if request.user != event.creator:
        return HttpResponseForbidden("You can only cancel your own events.")

    event.status = Event.Status.CANCELLED
    event.save()
    return redirect("events:event_detail", pk=event.pk)


@login_required
@require_POST
def event_rsvp(request, pk):
    event = get_object_or_404(Event, pk=pk)

    if event.status == Event.Status.CANCELLED:
        return HttpResponseForbidden("Cannot RSVP to a cancelled event.")

    RSVP.objects.get_or_create(user=request.user, event=event)
    return redirect("events:event_detail", pk=event.pk)


@login_required
@require_POST
def event_rsvp_cancel(request, pk):
    event = get_object_or_404(Event, pk=pk)
    RSVP.objects.filter(user=request.user, event=event).delete()
    return redirect("events:event_detail", pk=event.pk)


def event_list(request):
    return render(request, "events/event_list.html")
