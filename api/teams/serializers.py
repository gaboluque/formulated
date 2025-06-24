from rest_framework import serializers
from teams.models import Team, Member

class TeamMemberSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='member-detail')
    
    class Meta:
        model = Member
        fields = [
            'url', 'id', 'name', 'role', 'description', 'created_at', 'updated_at',
            # Driver-specific fields
            'driver_number', 'name_acronym', 'country_code', 'headshot_url'
        ]

class TeamSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='team-detail')
    members = TeamMemberSerializer(many=True, read_only=True)
    
    class Meta:
        model = Team
        fields = [
            'url', 'id', 'name', 'description', 'status', 'members', 'created_at', 'updated_at',
            # Basic team information
            'logo_url', 'base', 'first_team_entry',
            # Performance statistics
            'world_championships', 'highest_race_finish', 'pole_positions', 'fastest_laps',
            # Management
            'president', 'director', 'technical_manager',
            # Technical specifications
            'chassis', 'engine', 'tyres'
        ]

class MemberSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='member-detail')
    team = TeamSerializer(read_only=True)
    team_url = serializers.HyperlinkedRelatedField(view_name='team-detail', source='team', read_only=True)
        
    class Meta:
        model = Member
        fields = [
            'url', 'id', 'name', 'role', 'description', 'team', 'team_url', 'created_at', 'updated_at',
            # Driver-specific fields
            'driver_number', 'name_acronym', 'country_code', 'headshot_url'
        ]
