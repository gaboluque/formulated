from rest_framework import serializers
from races.models import Circuit, Race, Position


class CircuitRaceSerializer(serializers.ModelSerializer):
    """Simplified race serializer for use within circuit details"""
    url = serializers.HyperlinkedIdentityField(view_name='race-detail')
    
    class Meta:
        model = Race
        fields = [
            'url', 'id', 'name', 'description', 'start_at', 'status', 'created_at', 'updated_at'
        ]


class CircuitSerializer(serializers.HyperlinkedModelSerializer):
    """Circuit serializer with associated races"""
    url = serializers.HyperlinkedIdentityField(view_name='circuit-detail')
    races = CircuitRaceSerializer(many=True, read_only=True)
    races_count = serializers.SerializerMethodField()
    upcoming_races_count = serializers.SerializerMethodField()
    completed_races_count = serializers.SerializerMethodField()

    class Meta:
        model = Circuit
        fields = [
            'url', 'id', 'name', 'location', 
            'races', 'races_count', 'upcoming_races_count', 'completed_races_count',
            'created_at', 'updated_at'
        ]
    
    def get_races_count(self, obj):
        return obj.races.count()
    
    def get_upcoming_races_count(self, obj):
        from races.models import RaceStatus
        return obj.races.filter(status__in=[RaceStatus.SCHEDULED, RaceStatus.ONGOING]).count()
    
    def get_completed_races_count(self, obj):
        from races.models import RaceStatus
        return obj.races.filter(status=RaceStatus.COMPLETED).count()


class RacePositionSerializer(serializers.ModelSerializer):
    """Simplified position serializer for use within race details"""
    url = serializers.HyperlinkedIdentityField(view_name='position-detail')
    driver_url = serializers.HyperlinkedRelatedField(view_name='member-detail', source='driver', read_only=True)
    driver_name = serializers.CharField(source='driver.name', read_only=True)
    driver_number = serializers.CharField(source='driver.driver_number', read_only=True)
    driver_acronym = serializers.CharField(source='driver.name_acronym', read_only=True)
    team_name = serializers.CharField(source='driver.team.name', read_only=True)
    team_url = serializers.HyperlinkedRelatedField(view_name='team-detail', source='driver.team', read_only=True)
    
    class Meta:
        model = Position
        fields = [
            'url', 'id', 'position', 'points', 
            'driver_url', 'driver_name', 'driver_number', 'driver_acronym',
            'team_name', 'team_url',
            'created_at', 'updated_at'
        ]


class RaceSerializer(serializers.HyperlinkedModelSerializer):
    """Race serializer with circuit and position details"""
    url = serializers.HyperlinkedIdentityField(view_name='race-detail')
    circuit = CircuitSerializer(read_only=True)
    circuit_url = serializers.HyperlinkedRelatedField(view_name='circuit-detail', source='circuit', read_only=True)
    positions = RacePositionSerializer(many=True, read_only=True)
    positions_count = serializers.SerializerMethodField()
    is_finished = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Race
        fields = [
            'url', 'id', 'name', 'description', 'start_at', 'status', 'is_finished',
            'circuit', 'circuit_url', 
            'positions', 'positions_count',
            'created_at', 'updated_at'
        ]
    
    def get_positions_count(self, obj):
        return obj.positions.count()

class PositionSerializer(serializers.HyperlinkedModelSerializer):
    """Full position serializer with race and driver details"""
    url = serializers.HyperlinkedIdentityField(view_name='position-detail')
    race = RaceSerializer(read_only=True)
    race_url = serializers.HyperlinkedRelatedField(view_name='race-detail', source='race', read_only=True)
    driver_url = serializers.HyperlinkedRelatedField(view_name='member-detail', source='driver', read_only=True)
    driver_name = serializers.CharField(source='driver.name', read_only=True)
    driver_number = serializers.CharField(source='driver.driver_number', read_only=True)
    driver_acronym = serializers.CharField(source='driver.name_acronym', read_only=True)
    team_name = serializers.CharField(source='driver.team.name', read_only=True)
    team_url = serializers.HyperlinkedRelatedField(view_name='team-detail', source='driver.team', read_only=True)
    
    class Meta:
        model = Position
        fields = [
            'url', 'id', 'position', 'points',
            'race', 'race_url',
            'driver_url', 'driver_name', 'driver_number', 'driver_acronym',
            'team_name', 'team_url',
            'created_at', 'updated_at'
        ] 