from rest_framework import viewsets

from teams.models import Team, Member
from teams.serializers import TeamSerializer, MemberSerializer
from interactions.recordMixins import RecordMixin

class TeamViewSet(RecordMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Team.objects.all().order_by('name')
    serializer_class = TeamSerializer


class MemberViewSet(RecordMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Member.objects.all().order_by('name')
    serializer_class = MemberSerializer
