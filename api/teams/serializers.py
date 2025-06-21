from rest_framework import serializers
from teams.models import Team, Member

class TeamSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='team-detail')
    
    class Meta:
        model = Team
        fields = ['url', 'id', 'name', 'description', 'status', 'created_at', 'updated_at']

class MemberSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='member-detail')
    
    class Meta:
        model = Member
        fields = ['url', 'id', 'name', 'role', 'description', 'team', 'created_at', 'updated_at']