from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Assignee(models.Model):
    """Model to store assignee information for auto-population"""
    name = models.CharField(max_length=200, unique=True)
    email = models.EmailField()
    location = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        
    def __str__(self):
        return f"{self.name} ({self.email})"


class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    TITLE_CHOICES = [
        ('Create a document for Adult classes', 'Create a document for Adult classes'),
        ('Organize cultural event', 'Organize cultural event'),
        ('Coordinate volunteer training', 'Coordinate volunteer training'),
        ('Manage social media accounts', 'Manage social media accounts'),
        ('Prepare presentation materials', 'Prepare presentation materials'),
        ('Coordinate fundraising campaign', 'Coordinate fundraising campaign'),
        ('Organize community outreach', 'Organize community outreach'),
        ('Manage website content', 'Manage website content'),
        ('Coordinate language classes', 'Coordinate language classes'),
        ('Organize youth programs', 'Organize youth programs'),
        ('Other', 'Other'),
    ]
    
    title = models.CharField(max_length=200, choices=TITLE_CHOICES, default='Create a document for Adult classes')
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    
    # Owner/Creator
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    
    # Assigned By (new field)
    assigned_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tasks')
    
    # Assignee Information
    assignee_name = models.CharField(max_length=200, blank=True, null=True)
    assignee_email = models.EmailField(blank=True, null=True)
    assignee_location = models.CharField(max_length=200, blank=True, null=True)
    
    # Dates
    start_date = models.DateTimeField(null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        assignee_info = f" -> {self.assignee_name}" if self.assignee_name else ""
        return f"{self.title} - {self.owner.username} ({self.status}){assignee_info}"
    
    def get_priority_badge_class(self):
        """Return CSS class for priority badge"""
        return {
            'low': 'badge-secondary',
            'medium': 'badge-primary',
            'high': 'badge-warning',
            'urgent': 'badge-danger'
        }.get(self.priority, 'badge-primary')