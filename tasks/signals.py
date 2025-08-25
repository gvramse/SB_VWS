from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import Task
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Task)
def task_saved_handler(sender, instance, created, **kwargs):
    """Send email notification when a task is created or updated"""
    if not getattr(settings, 'TASK_EMAIL_NOTIFICATIONS', True):
        return
    
    try:
        # Determine if this is creation or update
        action = "created" if created else "updated"
        
        # Get recipient email
        recipient_email = instance.assignee_email
        if not recipient_email:
            logger.info(f"Task {instance.id} has no assignee email, skipping notification")
            return
        
        # Prepare email context
        context = {
            'task': instance,
            'action': action,
            'created': created,
            'owner_name': f"{instance.owner.first_name} {instance.owner.last_name}".strip() or instance.owner.username,
        }
        
        # Create subject
        if created:
            subject = f"New Task Assigned: {instance.title}"
        else:
            subject = f"Task Updated: {instance.title}"
        
        # Create email content
        html_message = render_to_string('emails/task_notification.html', context)
        plain_message = strip_tags(html_message)
        
        # Send email
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient_email],
            html_message=html_message,
            fail_silently=False,
        )
        
        logger.info(f"Task {action} notification sent to {recipient_email} for task: {instance.title}")
        
    except Exception as e:
        logger.error(f"Failed to send task {action} notification: {str(e)}")


@receiver(post_delete, sender=Task)
def task_deleted_handler(sender, instance, **kwargs):
    """Send email notification when a task is deleted"""
    if not getattr(settings, 'TASK_EMAIL_NOTIFICATIONS', True):
        return
    
    try:
        # Get recipient email
        recipient_email = instance.assignee_email
        if not recipient_email:
            logger.info(f"Deleted task had no assignee email, skipping notification")
            return
        
        # Prepare email context
        context = {
            'task': instance,
            'action': 'deleted',
            'owner_name': f"{instance.owner.first_name} {instance.owner.last_name}".strip() or instance.owner.username,
        }
        
        # Create subject
        subject = f"Task Deleted: {instance.title}"
        
        # Create email content
        html_message = render_to_string('emails/task_notification.html', context)
        plain_message = strip_tags(html_message)
        
        # Send email
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient_email],
            html_message=html_message,
            fail_silently=False,
        )
        
        logger.info(f"Task deletion notification sent to {recipient_email} for task: {instance.title}")
        
    except Exception as e:
        logger.error(f"Failed to send task deletion notification: {str(e)}")
