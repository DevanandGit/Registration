from rest_framework import serializers
from .models import Events, Delegates, DelegateEvent

class EventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = '__all__'


class DelegateEventSerializer(serializers.ModelSerializer):
    event = EventsSerializer()  # Nested serializer for event details

    class Meta:
        model = DelegateEvent
        fields = ('event', 'is_active')


class DelegatesSerializer(serializers.ModelSerializer):
    events = DelegateEventSerializer(many=True, read_only = True)  # Nested serializer for delegate's events

    class Meta:
        model = Delegates
        fields = ('id', 'name', 'semester', 'ktu_id', 'gmail','events', 'total_amount')

