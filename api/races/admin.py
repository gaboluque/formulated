from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from django.contrib import messages
from datetime import datetime
from races.models import Circuit, Race, Position
from data_loader.services.races_puller import RacesPuller

@admin.register(Circuit)
class CircuitAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'races_count', 'created_at', 'updated_at')
    search_fields = ('name', 'location')
    list_filter = ('created_at', 'updated_at')
    ordering = ('name',)
    
    def races_count(self, obj):
        return obj.races.count()
    races_count.short_description = 'Races'

@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'circuit', 'status', 'start_at', 'created_at', 'updated_at')
    search_fields = ('name', 'circuit__name', 'description')
    list_filter = ('status', 'start_at', 'circuit', 'created_at', 'updated_at')
    list_select_related = ('circuit',)
    ordering = ('-start_at',)
    
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('pull-races/', self.admin_site.admin_view(self.pull_races), name='races_race_pull-races'),
            path('pull-races/<int:season>/', self.admin_site.admin_view(self.pull_races), name='races_race_pull-races-season'),
        ]
        return my_urls + urls

    def pull_races(self, request, season=None):
        try:
            if season is None:
                season = datetime.now().year
                
            puller = RacesPuller()
            result = puller.pull_and_sync_races(season)

            if result['success']:
                message = f"Successfully synced {result['races_fetched']} races from APISports F1 API for {season} season. "
                message += f"Races - Created: {result['races_created']}, Updated: {result['races_updated']}. "
                message += f"Circuits - Created: {result['circuits_created']}, Updated: {result['circuits_updated']}"
                if result['errors']:
                    message += f". Errors: {len(result['errors'])}"
                messages.success(request, message)
            else:
                error_message = f"Failed to sync races for {season} season"
                if result['errors']:
                    error_message += f": {'; '.join(result['errors'][:3])}"  # Show first 3 errors
                messages.error(request, error_message)
                
        except Exception as e:
            messages.error(request, f"Error pulling races: {str(e)}")
        
        return redirect('admin:races_race_changelist')

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('race', 'driver', 'position', 'points', 'created_at', 'updated_at')
    search_fields = ('race__name', 'driver__name')
    list_filter = ('race', 'position', 'points', 'created_at', 'updated_at')
    list_select_related = ('race', 'driver')
    ordering = ('race', 'position')
