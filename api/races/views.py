from rest_framework import viewsets
from django.db.models import Prefetch

from races.models import Circuit, Race, Position, RaceStatus
from races.serializers import CircuitSerializer, RaceSerializer, PositionSerializer
from interactions.recordMixins import RecordMixin


class CircuitViewSet(RecordMixin, viewsets.ReadOnlyModelViewSet):
    """Circuit viewset with optimized queries and filtering"""
    queryset = Circuit.objects.prefetch_related('races').order_by('name')
    serializer_class = CircuitSerializer
    
    def get_queryset(self):
        # Start with the base queryset
        queryset = self.queryset
        
        # Filter by location if provided
        location = self.request.query_params.get('location')
        if location:
            queryset = queryset.filter(location__icontains=location)
        
        return queryset


class RaceViewSet(RecordMixin, viewsets.ReadOnlyModelViewSet):
    """Race viewset with optimized queries and comprehensive filtering"""
    queryset = Race.objects.select_related('circuit').prefetch_related(
        Prefetch(
            'positions',
            queryset=Position.objects.select_related('driver', 'driver__team').order_by('position')
        )
    ).order_by('-start_at')
    serializer_class = RaceSerializer

    def get_queryset(self):
        # Start with the base queryset
        queryset = self.queryset
        
        # Filter by circuit
        circuit_id = self.request.query_params.get('circuit_id')
        if circuit_id:
            queryset = queryset.filter(circuit_id=circuit_id)
        
        # Filter by status
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        # Filter by year
        year = self.request.query_params.get('year')
        if year:
            queryset = queryset.filter(start_at__year=year)
        
        # Filter by season (alias for year)
        season = self.request.query_params.get('season')
        if season:
            queryset = queryset.filter(start_at__year=season)
        
        # Filter upcoming races
        upcoming = self.request.query_params.get('upcoming')
        if upcoming and upcoming.lower() in ['true', '1']:
            queryset = queryset.filter(status__in=[RaceStatus.SCHEDULED, RaceStatus.ONGOING])
        
        # Filter completed races
        completed = self.request.query_params.get('completed')
        if completed and completed.lower() in ['true', '1']:
            queryset = queryset.filter(status=RaceStatus.COMPLETED)
        
        return queryset


class PositionViewSet(viewsets.ReadOnlyModelViewSet):
    """Position viewset with optimized queries and filtering"""
    queryset = Position.objects.select_related(
        'race', 'race__circuit', 'driver', 'driver__team'
    ).order_by('race__start_at', 'position')
    serializer_class = PositionSerializer
    
    def get_queryset(self):
        # Start with the base queryset
        queryset = self.queryset
        
        # Filter by race
        race_id = self.request.query_params.get('race_id')
        if race_id:
            queryset = queryset.filter(race_id=race_id)
        
        # Filter by driver
        driver_id = self.request.query_params.get('driver_id')
        if driver_id:
            queryset = queryset.filter(driver_id=driver_id)
        
        # Filter by team
        team_id = self.request.query_params.get('team_id')
        if team_id:
            queryset = queryset.filter(driver__team_id=team_id)
        
        # Filter by position (e.g., winners only)
        position = self.request.query_params.get('position')
        if position:
            queryset = queryset.filter(position=position)
        
        # Filter by year/season
        year = self.request.query_params.get('year')
        if year:
            queryset = queryset.filter(race__start_at__year=year)
        
        season = self.request.query_params.get('season')
        if season:
            queryset = queryset.filter(race__start_at__year=season)
        
        # Filter by points threshold
        min_points = self.request.query_params.get('min_points')
        if min_points:
            queryset = queryset.filter(points__gte=min_points)
        
        return queryset
