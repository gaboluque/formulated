from django.contrib import admin
from races.models import Circuit, Race, Position

@admin.register(Circuit)
class CircuitAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'created_at', 'updated_at')
    search_fields = ('name', 'location')
    list_filter = ('created_at', 'updated_at')

@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'circuit', 'start_at', 'created_at', 'updated_at')
    search_fields = ('name', 'circuit__name')
    list_filter = ('start_at', 'circuit', 'created_at', 'updated_at')
    list_select_related = ('circuit',)

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('race', 'driver', 'position', 'points', 'created_at', 'updated_at')
    search_fields = ('race__name', 'driver__name')
    list_filter = ('race', 'position', 'points', 'created_at', 'updated_at')
    list_select_related = ('race', 'driver')
    ordering = ('race', 'position')
