from rest_framework import viewsets
from events.models import Event, RSVP
from .serializers import EventSerializer, RSVPSerializer

class EventViewSet(viewsets.ModelViewSet):
    """GET, POST, PUT, DELETE events"""
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class RSVPViewSet(viewsets.ModelViewSet):
    """GET, POST, PUT, DELETE RSVPs"""
    queryset = RSVP.objects.all()
    serializer_class = RSVPSerializer