from rest_framework import serializers
from races.models import Circuit, Race, Position
from teams.serializers import MemberSerializer

class CircuitSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='circuit-detail')

    class Meta:
        model = Circuit
        fields = ['url', 'id', 'name', 'location', 'created_at', 'updated_at']

class PositionSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='position-detail')
    race_url = serializers.HyperlinkedRelatedField(view_name='race-detail', source='race', read_only=True)
    driver = MemberSerializer(read_only=True)
    
    class Meta:
        model = Position
        fields = ['url', 'id', 'race', 'race_url', 'driver', 'position', 'points', 'created_at', 'updated_at']

class RaceSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='race-detail')
    circuit = CircuitSerializer(read_only=True)
    circuit_url = serializers.HyperlinkedRelatedField(view_name='circuit-detail', source='circuit', read_only=True)
    positions = PositionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Race
        fields = ['url', 'id', 'name', 'description', 'circuit', 'circuit_url', 'start_at', 'status', 'positions', 'created_at', 'updated_at'] 