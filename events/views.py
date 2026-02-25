from decimal import Decimal, InvalidOperation  # noqa
from django.contrib.auth.decorators import login_required
from django.db.models import Count  # noqa
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST


from .forms import EventForm
from .models import RSVP, Event, Category  # noqa


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
    events = Event.objects.select_related("category", "creator")

    # --- Filters ---

    category_id = request.GET.get("category")
    if category_id:
        events = events.filter(category_id=category_id)

    date_from = request.GET.get("date_from")
    if date_from:
        events = events.filter(date_time__date__gte=date_from)

    date_to = request.GET.get("date_to")
    if date_to:
        events = events.filter(date_time__date__lte=date_to)

    price_max = request.GET.get("price_max")
    if price_max:
        try:
            events = events.filter(price__lte=Decimal(price_max))
        except InvalidOperation:
            pass  # Ignore invalid decimal input

    free_only = request.GET.get("free_only")
    if free_only:
        events = events.filter(price=Decimal("0.00"))

    # Auth-required filters: silently skip if not logged in
    if request.user.is_authenticated:
        my_events = request.GET.get("my_events")
        if my_events:
            events = events.filter(creator=request.user)

        my_rsvps = request.GET.get("my_rsvps")
        if my_rsvps:
            events = events.filter(rsvps__user=request.user)

    # --- Sorting ---

    # Always annotate attendee count so we can display it and sort by it
    events = events.annotate(attendee_count=Count("rsvps"))

    sort_field = request.GET.get("sort", "")
    sort_dir = request.GET.get("dir", "asc")

    sort_map = {
        "date": "date_time",
        "price": "price",
        "location": "location",
        "attendees": "attendee_count",
    }

    if sort_field in sort_map:
        order_field = sort_map[sort_field]
        if sort_dir == "desc":
            order_field = f"-{order_field}"
        events = events.order_by(order_field)
    # else: default ordering from Meta (date_time ascending)

    # --- Template context ---

    categories = Category.objects.all()

    # Preserve current filter/sort values for form repopulation and sort toggle
    current_filters = {
        "category": category_id or "",
        "date_from": date_from or "",
        "date_to": date_to or "",
        "price_max": price_max or "",
        "free_only": free_only or "",
        "my_events": request.GET.get("my_events", ""),
        "my_rsvps": request.GET.get("my_rsvps", ""),
    }

    current_sort = {
        "field": sort_field,
        "dir": sort_dir if sort_field else "",
    }

    return render(
        request,
        "events/event_list.html",
        {
            "events": events,
            "categories": categories,
            "current_filters": current_filters,
            "current_sort": current_sort,
        },
    )
