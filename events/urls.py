from django.shortcuts import render
from django.urls import path

app_name = "events"


def event_list(request):
    """Placeholder — replaced in Phase 2 (REQ-12)."""
    return render(request, "events/event_list.html")


urlpatterns = [
    path("", event_list, name="event_list"),
]
