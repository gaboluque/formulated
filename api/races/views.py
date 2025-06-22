from rest_framework import viewsets

from races.models import Circuit, Race, Position
from races.serializers import CircuitSerializer, RaceSerializer, PositionSerializer
from interactions.recordMixins import RecordMixin

class CircuitViewSet(RecordMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Circuit.objects.all().order_by('name')
    serializer_class = CircuitSerializer

class RaceViewSet(RecordMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Race.objects.all().order_by('start_at')
    serializer_class = RaceSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        circuit_id = self.request.query_params.get('circuit_id')
        
        if circuit_id:
            queryset = queryset.filter(circuit_id=circuit_id)
        
        return queryset

class PositionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Position.objects.all().order_by('race', 'position')
    serializer_class = PositionSerializer
