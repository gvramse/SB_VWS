from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from tasks.models import Task
import random


class Command(BaseCommand):
    help = 'Populate the database with sample tasks for testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=20,
            help='Number of sample tasks to create',
        )

    def handle(self, *args, **options):
        count = options['count']
        
        # Sample data
        sample_titles = [
            "Implement user authentication system",
            "Design database schema for inventory",
            "Create REST API endpoints",
            "Update website frontend design",
            "Fix bug in payment processing",
            "Optimize database queries",
            "Write unit tests for core modules",
            "Deploy application to production",
            "Conduct security audit",
            "Update documentation",
            "Set up monitoring and alerts",
            "Refactor legacy code",
            "Implement caching layer",
            "Create mobile app wireframes",
            "Update third-party dependencies",
            "Configure backup systems",
            "Train new team members",
            "Conduct code review",
            "Plan sprint retrospective",
            "Research new technologies"
        ]
        
        sample_descriptions = [
            "This task requires careful planning and execution to ensure all requirements are met.",
            "Please coordinate with the team lead before starting this task.",
            "High priority task that needs to be completed by the end of the week.",
            "This is a complex task that may require additional resources.",
            "Follow the established coding standards and best practices.",
            "Ensure proper testing before marking this task as complete.",
            "Document all changes and update relevant wikis.",
            "Consider performance implications when implementing this feature.",
            "Review similar implementations in other projects for reference.",
            "This task is part of a larger initiative - coordinate with other teams."
        ]
        
        sample_assignees = [
            {"name": "John Smith", "email": "john.smith@example.com", "location": "New York, USA"},
            {"name": "Sarah Johnson", "email": "sarah.johnson@example.com", "location": "London, UK"},
            {"name": "Mike Chen", "email": "mike.chen@example.com", "location": "San Francisco, USA"},
            {"name": "Emily Davis", "email": "emily.davis@example.com", "location": "Toronto, Canada"},
            {"name": "Alex Wilson", "email": "alex.wilson@example.com", "location": "Sydney, Australia"},
            {"name": "Maria Garcia", "email": "maria.garcia@example.com", "location": "Madrid, Spain"},
            {"name": "David Brown", "email": "david.brown@example.com", "location": "Berlin, Germany"},
            {"name": "Lisa Anderson", "email": "lisa.anderson@example.com", "location": "Tokyo, Japan"},
            {"name": "Tom Miller", "email": "tom.miller@example.com", "location": "Chicago, USA"},
            {"name": "Jennifer Taylor", "email": "jennifer.taylor@example.com", "location": "Mumbai, India"}
        ]
        
        # Get or create a default user
        user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'first_name': 'Admin',
                'last_name': 'User',
                'is_staff': True,
                'is_superuser': True
            }
        )
        
        if created:
            user.set_password('admin123')
            user.save()
            self.stdout.write(
                self.style.SUCCESS(f'Created admin user: admin/admin123')
            )
        
        # Create sample tasks
        created_count = 0
        now = timezone.now()
        
        for i in range(count):
            # Random data selection
            title = random.choice(sample_titles)
            description = random.choice(sample_descriptions)
            assignee = random.choice(sample_assignees)
            
            # Random dates
            start_date = now + timedelta(days=random.randint(-30, 7))
            due_date = start_date + timedelta(days=random.randint(1, 30))
            
            # Random priority and status
            priority = random.choice(['low', 'medium', 'high', 'urgent'])
            status = random.choice(['pending', 'in_progress', 'completed', 'cancelled'])
            
            # Create task
            task = Task.objects.create(
                title=f"{title} #{i+1}",
                description=description,
                status=status,
                priority=priority,
                owner=user,
                assignee_name=assignee['name'],
                assignee_email=assignee['email'],
                assignee_location=assignee['location'],
                start_date=start_date,
                due_date=due_date,
            )
            
            created_count += 1
            
            if created_count % 5 == 0:
                self.stdout.write(f'Created {created_count} tasks...')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {created_count} sample tasks!'
            )
        )
        
        # Summary
        self.stdout.write('\nTask Summary:')
        for status_value, status_label in Task.STATUS_CHOICES:
            count = Task.objects.filter(status=status_value).count()
            self.stdout.write(f'  {status_label}: {count} tasks')
        
        self.stdout.write('\nPriority Summary:')
        for priority_value, priority_label in Task.PRIORITY_CHOICES:
            count = Task.objects.filter(priority=priority_value).count()
            self.stdout.write(f'  {priority_label}: {count} tasks')
