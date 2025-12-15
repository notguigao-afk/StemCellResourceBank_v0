from django.contrib import admin
from django.utils.html import format_html
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


# Register the Historical Sample model for viewing ALL history including deleted samples
from samples.models import Sample
HistoricalSample = Sample.history.model

@admin.register(HistoricalSample)
class HistoricalSampleAdmin(admin.ModelAdmin):
    """Admin view for all sample history including deleted samples"""
    list_display = (
        'sample_id',
        'name',
        'history_type_display',
        'history_user',
        'history_date',
    )
    list_filter = ('history_type', 'sample_type', 'status', 'history_date')
    search_fields = ('sample_id', 'name', 'description')
    readonly_fields = [field.name for field in HistoricalSample._meta.fields]
    ordering = ('-history_date',)
    
    def history_type_display(self, obj):
        """Display history type with color coding"""
        type_map = {
            '+': ('Created', 'green'),
            '~': ('Modified', 'orange'),
            '-': ('Deleted', 'red'),
        }
        label, color = type_map.get(obj.history_type, ('Unknown', 'gray'))
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color, label
        )
    history_type_display.short_description = 'Action'
    history_type_display.admin_order_field = 'history_type'
    
    def has_add_permission(self, request):
        return False  # Cannot add history manually
    
    def has_change_permission(self, request, obj=None):
        return False  # Cannot edit history
    
    def has_delete_permission(self, request, obj=None):
        return False  # Cannot delete history (audit trail!)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'updated_at')
    
    def has_add_permission(self, request):
        # Only allow one instance
        return not SiteSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False
