from django.contrib import admin
from .models import Review, Like


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Admin configuration for Review model"""
    list_display = ['user', 'rating', 'record_type', 'record_object', 'created_at']
    list_filter = ['rating', 'record_type', 'created_at']
    search_fields = ['user__username', 'description', 'record_type__model']
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Review Information', {
            'fields': ('user', 'rating', 'description')
        }),
        ('Record Information', {
            'fields': ('record_type', 'record_id')
        }),
        ('Metadata', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def record_object(self, obj):
        """Display the record object in admin list"""
        return str(obj.record) if obj.record else 'N/A'
    record_object.short_description = 'Record'


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    """Admin configuration for Like model"""
    list_display = ['user', 'record_type', 'record_object', 'created_at']
    list_filter = ['record_type', 'created_at']
    search_fields = ['user__username', 'record_type__model']
    readonly_fields = ['id', 'created_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Like Information', {
            'fields': ('user',)
        }),
        ('Record Information', {
            'fields': ('record_type', 'record_id')
        }),
        ('Metadata', {
            'fields': ('id', 'created_at'),
            'classes': ('collapse',)
        }),
    )

    def record_object(self, obj):
        """Display the record object in admin list"""
        return str(obj.record) if obj.record else 'N/A'
    record_object.short_description = 'Record'
