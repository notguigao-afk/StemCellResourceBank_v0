from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Sample, SiteSettings


@admin.register(Sample)
class SampleAdmin(SimpleHistoryAdmin):
    list_display = (
        'sample_id', 
        'name', 
        'sample_type', 
        'status', 
        'quantity', 
        'storage_location',
        'created_by',
        'created_at'
    )
    list_filter = ('sample_type', 'status', 'research_use_only', 'created_at')
    search_fields = ('sample_id', 'name', 'description', 'source', 'storage_location')
    readonly_fields = ('created_at', 'updated_at', 'created_by')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('sample_id', 'name', 'sample_type', 'description')
        }),
        ('Source and Donor', {
            'fields': ('source', 'donor_info')
        }),
        ('Storage', {
            'fields': ('storage_location', 'status', 'quantity', 'passage_number')
        }),
        ('Dates', {
            'fields': ('collection_date', 'storage_date', 'expiration_date')
        }),
        ('Quality', {
            'fields': ('viability', 'quality_control_notes')
        }),
        ('Additional Information', {
            'fields': ('research_use_only', 'image')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating a new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'updated_at')
    
    def has_add_permission(self, request):
        # Only allow one instance
        return not SiteSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False
