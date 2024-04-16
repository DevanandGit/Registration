from rest_framework import serializers
from .models import Events, Delegates, DelegateEvent, Entertainment, DelegateEntertainment

class EntertainmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entertainment
        fields = '__all__'

class EventsSerializer(serializers.ModelSerializer):
    games = EntertainmentSerializer(many = True, read_only = True)
    class Meta:
        model = Events
        fields = '__all__'


class DelegateEventSerializer(serializers.ModelSerializer):
    event = EventsSerializer()  # Nested serializer for event details

    class Meta:
        model = DelegateEvent
        fields = ('event', 'is_active')


class DelegateEntertainmentSerializer(serializers.ModelSerializer):
    # entertainment = EventsSerializer(many = True, read_only = True)  # Nested serializer for event details

    class Meta:
        model = DelegateEntertainment
        fields = ('entertainment', 'start_time', 'end_time', 'is_active')


class DelegatesSerializer(serializers.ModelSerializer):
    events = DelegateEventSerializer(many=True, read_only = True)  # Nested serializer for delegate's events
    entertainment = DelegateEntertainmentSerializer(many=True, read_only = True)
    class Meta:
        model = Delegates
        fields = ('id', 'name', 'semester', 'ktu_id', 'gmail','events', 'entertainment','total_amount')



