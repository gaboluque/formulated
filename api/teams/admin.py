from django.contrib import admin
from teams.models import Team, Member
from django.urls import path
from django.shortcuts import redirect
from django.contrib import messages
from data_loader.services.drivers_puller import DriversPuller

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_filter = ('status', 'created_at', 'updated_at')
    ordering = ('name',)

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'team', 'role', 'driver_number', 'name_acronym', 'created_at', 'updated_at')
    search_fields = ('name', 'team__name', 'description', 'name_acronym')
    list_filter = ('role', 'team', 'created_at', 'updated_at')
    list_select_related = ('team',)
    ordering = ('team', 'name')
    
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('pull-drivers/', self.admin_site.admin_view(self.pull_drivers), name='teams_member_pull-drivers'),
        ]
        return my_urls + urls
    
    def pull_drivers(self, request):
        try:            
            puller = DriversPuller()
            result = puller.pull_and_sync_drivers()
            
            if result['success']:
                message = f"Successfully synced {result['drivers_fetched']} drivers from OpenF1. "
                message += f"Created: {result['drivers_created']}, Updated: {result['drivers_updated']}"
                if result['errors']:
                    message += f", Errors: {len(result['errors'])}"
                messages.success(request, message)
            else:
                error_message = "Failed to sync drivers"
                if result['errors']:
                    error_message += f": {'; '.join(result['errors'][:3])}"  # Show first 3 errors
                messages.error(request, error_message)
                
        except Exception as e:
            messages.error(request, f"Error pulling drivers: {str(e)}")
        
        return redirect('admin:teams_member_changelist')