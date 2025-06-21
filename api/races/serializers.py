from rest_framework import serializers
from races.models import Circuit, Race, Position

class CircuitSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='circuit-detail')

    class Meta:
        model = Circuit
        fields = ['url', 'id', 'name', 'location', 'created_at', 'updated_at']

class RaceSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='race-detail')
    circuit_url = serializers.HyperlinkedRelatedField(view_name='circuit-detail', source='circuit', read_only=True)
    
    class Meta:
        model = Race
        fields = ['url', 'id', 'name', 'circuit', 'circuit_url', 'start_at', 'created_at', 'updated_at']

class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__' 