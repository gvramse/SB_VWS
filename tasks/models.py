from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


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
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    
    # Owner/Creator
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    
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