from django.http import HttpResponse
from django.urls import path

app_name = "events"


def event_list(request):
    """Placeholder — replaced in Phase 2 (REQ-12)."""
    return HttpResponse("<h1>Events</h1><p>Coming soon.</p>")


urlpatterns = [
    path("", event_list, name="event_list"),
]
