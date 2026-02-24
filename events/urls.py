from django.urls import path

from . import views

app_name = "events"


urlpatterns = [
    path("", views.event_list, name="event_list"),
    path("create/", views.event_create, name="event_create"),
    path("<int:pk>/", views.event_detail, name="event_detail"),
    path("<int:pk>/edit/", views.event_edit, name="event_edit"),
    path("<int:pk>/cancel/", views.event_cancel, name="event_cancel"),
    path("<int:pk>/rsvp/", views.event_rsvp, name="event_rsvp"),
    path("<int:pk>/rsvp/cancel/", views.event_rsvp_cancel, name="event_rsvp_cancel"),
]
