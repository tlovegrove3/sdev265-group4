from rest_framework import viewsets, permissions
from events.models import Event, RSVP
from .serializers import EventSerializer, RSVPSerializer
from .permissions import IsOwnerOrReadOnly

class EventViewSet(viewsets.ModelViewSet):
    """GET, POST, PUT, DELETE events"""
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    ]

class RSVPViewSet(viewsets.ModelViewSet):
    """GET, POST, PUT, DELETE RSVPs"""
    queryset = RSVP.objects.all()
    serializer_class = RSVPSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]