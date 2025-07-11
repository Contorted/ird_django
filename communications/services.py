import logging
from django.core.mail import send_mail
from django.template import Template, Context
from django.conf import settings
from django.utils import timezone
from .models import EmailTemplate, EmailLog

logger = logging.getLogger(__name__)

class EmailService:
    """Service for sending emails with templates"""
    
    def __init__(self):
        self.from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'clayton.lake.davidson@gmail.com')
    
    def send_templated_email(self, template_type, recipient_email, context_data, user=None, meeting=None):
        """
        Send an email using a template
        
        Args:
            template_type: Type of email template (e.g., 'welcome', 'meeting_confirmation')
            recipient_email: Email address to send to
            context_data: Dictionary of variables for template rendering
            user: User object (optional, for logging)
            meeting: Meeting object (optional, for logging)
        """
        try:
            # Get the email template
            template = EmailTemplate.objects.get(
                template_type=template_type,
                is_active=True
            )
        except EmailTemplate.DoesNotExist:
            logger.error(f"Email template '{template_type}' not found")
            return False
        
        # Create email log entry
        email_log = EmailLog.objects.create(
            recipient=recipient_email,
            subject=template.subject,
            template_type=template_type,
            user=user,
            meeting=meeting,
            status='pending'
        )
        
        try:
            # Render the template with context
            subject_template = Template(template.subject)
            html_template = Template(template.html_content)
            text_template = Template(template.text_content)
            
            django_context = Context(context_data)
            
            rendered_subject = subject_template.render(django_context)
            rendered_html = html_template.render(django_context)
            rendered_text = text_template.render(django_context)
            
            # Send the email
            success = send_mail(
                subject=rendered_subject,
                message=rendered_text,
                from_email=self.from_email,
                recipient_list=[recipient_email],
                html_message=rendered_html,
                fail_silently=False
            )
            
            if success:
                email_log.status = 'sent'
                email_log.sent_at = timezone.now()
                logger.info(f"Email sent successfully to {recipient_email}")
            else:
                email_log.status = 'failed'
                email_log.error_message = "Failed to send email"
                logger.error(f"Failed to send email to {recipient_email}")
            
            email_log.save()
            return success
            
        except Exception as e:
            email_log.status = 'failed'
            email_log.error_message = str(e)
            email_log.save()
            logger.error(f"Error sending email to {recipient_email}: {str(e)}")
            return False
    
    def send_welcome_email(self, user):
        """Send welcome email to new user"""
        context = {
            'user_name': user.get_full_name() or user.username,
            'user_email': user.email,
            'login_url': f"{settings.SITE_URL}/accounts/login/",
            'dashboard_url': f"{settings.SITE_URL}/dashboard/",
            'meetings_url': f"{settings.SITE_URL}/meetings/",
        }
        
        return self.send_templated_email(
            template_type='welcome',
            recipient_email=user.email,
            context_data=context,
            user=user
        )
    
    def send_meeting_confirmation(self, user, meeting):
        """Send meeting registration confirmation"""
        context = {
            'user_name': user.get_full_name() or user.username,
            'meeting_title': meeting.title,
            'meeting_date': meeting.start_datetime.strftime('%A, %B %d, %Y'),
            'meeting_time': meeting.start_datetime.strftime('%I:%M %p'),
            'meeting_type': meeting.get_meeting_type_display(),
            'meeting_location': meeting.location,
            'meeting_link': meeting.online_link,
            'meeting_description': meeting.description,
            'meeting_url': f"{settings.SITE_URL}/meetings/{meeting.slug}/",
            'organizer_name': meeting.created_by.get_full_name() or meeting.created_by.username,
        }
        
        return self.send_templated_email(
            template_type='meeting_confirmation',
            recipient_email=user.email,
            context_data=context,
            user=user,
            meeting=meeting
        )
    
    def send_meeting_reminder(self, user, meeting):
        """Send meeting reminder (24 hours before)"""
        context = {
            'user_name': user.get_full_name() or user.username,
            'meeting_title': meeting.title,
            'meeting_date': meeting.start_datetime.strftime('%A, %B %d, %Y'),
            'meeting_time': meeting.start_datetime.strftime('%I:%M %p'),
            'meeting_type': meeting.get_meeting_type_display(),
            'meeting_location': meeting.location,
            'meeting_link': meeting.online_link,
            'meeting_url': f"{settings.SITE_URL}/meetings/{meeting.slug}/",
        }
        
        return self.send_templated_email(
            template_type='meeting_reminder',
            recipient_email=user.email,
            context_data=context,
            user=user,
            meeting=meeting
        )

# Initialize the service
email_service = EmailService()