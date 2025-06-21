from django.contrib import admin
from teams.models import Team, Member

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_filter = ('status', 'created_at', 'updated_at')
    ordering = ('name',)

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'team', 'role', 'created_at', 'updated_at')
    search_fields = ('name', 'team__name', 'description')
    list_filter = ('role', 'team', 'created_at', 'updated_at')
    list_select_related = ('team',)
    ordering = ('team', 'name')