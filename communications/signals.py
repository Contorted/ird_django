from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from meetings.models import MeetingAttendance
from .services import email_service
import logging

logger = logging.getLogger(__name__)

User = get_user_model()

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    """Send welcome email when new user is created"""
    if created:
        try:
            email_service.send_welcome_email(instance)
            logger.info(f"Welcome email sent to {instance.email}")
        except Exception as e:
            logger.error(f"Failed to send welcome email to {instance.email}: {str(e)}")

@receiver(post_save, sender=MeetingAttendance)
def send_meeting_confirmation_email(sender, instance, created, **kwargs):
    """Send meeting confirmation when user registers for meeting"""
    if created and instance.status == 'registered':
        try:
            email_service.send_meeting_confirmation(instance.user, instance.meeting)
            logger.info(f"Meeting confirmation sent to {instance.user.email}")
        except Exception as e:
            logger.error(f"Failed to send meeting confirmation to {instance.user.email}: {str(e)}")