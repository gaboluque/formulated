from rest_framework import viewsets
from django.db.models import F

from teams.models import Team, Member
from teams.serializers import TeamSerializer, MemberSerializer
from interactions.recordMixins import RecordMixin

class TeamViewSet(RecordMixin, viewsets.ReadOnlyModelViewSet):
    # Order by world championships descending, nulls last
    queryset = Team.objects.all().order_by(F('world_championships').desc(nulls_last=True), 'name')
    serializer_class = TeamSerializer


class MemberViewSet(RecordMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Member.objects.all().order_by('driver_number', 'team__name', 'name')
    serializer_class = MemberSerializer
