from django.contrib import admin
from .models import Task, Assignee


@admin.register(Assignee)
class AssigneeAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'location', 'created_at']
    list_filter = ['location', 'created_at']
    search_fields = ['name', 'email', 'location']
    ordering = ['name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'email', 'location')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'assigned_by', 'assignee_name', 'status', 'priority', 'due_date', 'created_at']
    list_filter = ['status', 'priority', 'created_at', 'due_date', 'assignee_location']
    search_fields = ['title', 'description', 'assignee_name', 'assignee_email']
    list_editable = ['status', 'priority']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Task Information', {
            'fields': ('title', 'description', 'status', 'priority')
        }),
        ('Assignment', {
            'fields': ('owner', 'assigned_by', 'assignee_name', 'assignee_email', 'assignee_location')
        }),
        ('Dates', {
            'fields': ('start_date', 'due_date')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['created_at', 'updated_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('owner', 'assigned_by')