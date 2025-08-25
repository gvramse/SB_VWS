from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'assignee_name', 'status', 'priority', 'start_date', 'due_date']
    list_filter = ['status', 'priority', 'created_at', 'owner', 'assignee_location']
    search_fields = ['title', 'description', 'owner__username', 'assignee_name', 'assignee_email']
    list_editable = ['status', 'priority']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'status', 'priority', 'owner')
        }),
        ('Assignee Information', {
            'fields': ('assignee_name', 'assignee_email', 'assignee_location'),
            'classes': ('collapse',)
        }),
        ('Dates', {
            'fields': ('start_date', 'due_date', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    def has_change_permission(self, request, obj=None):
        # Only superusers can access admin panel
        return request.user.is_superuser
    
    def has_view_permission(self, request, obj=None):
        # Only superusers can access admin panel
        return request.user.is_superuser
    
    def has_add_permission(self, request):
        # Only superusers can access admin panel
        return request.user.is_superuser
    
    def has_delete_permission(self, request, obj=None):
        # Only superusers can access admin panel
        return request.user.is_superuser