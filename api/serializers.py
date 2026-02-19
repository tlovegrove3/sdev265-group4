from rest_framework import serializers
from events.models import Event, RSVP
from accounts.models import User

class EventSerializer(serializers.ModelSerializer):
    """Converts Event model to/from JSON"""
    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'date_time', 'location', 'price', 'creator']

class RSVPSerializer(serializers.ModelSerializer):
    """Converts RSVP model to/from JSON"""
    class Meta:
        model = RSVP
        fields = ['id', 'event', 'user', 'response']