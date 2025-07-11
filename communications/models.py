from django.db import models
from django.conf import settings

class EmailTemplate(models.Model):
    """Email templates for different types of notifications"""
    TEMPLATE_TYPES = [
        ('welcome', 'Welcome Email'),
        ('meeting_confirmation', 'Meeting Registration Confirmation'),
        ('meeting_reminder', 'Meeting Reminder'),
        ('meeting_cancellation', 'Meeting Cancellation'),
        ('password_reset', 'Password Reset'),
        ('admin_notification', 'Admin Notification'),
    ]
    
    name = models.CharField(max_length=100)
    template_type = models.CharField(max_length=30, choices=TEMPLATE_TYPES, unique=True)
    subject = models.CharField(max_length=200)
    html_content = models.TextField(help_text="HTML version of the email")
    text_content = models.TextField(help_text="Plain text version of the email")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.get_template_type_display()})"

class EmailLog(models.Model):
    """Log of sent emails for tracking and debugging"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
    ]
    
    recipient = models.EmailField()
    subject = models.CharField(max_length=200)
    template_type = models.CharField(max_length=30)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    error_message = models.TextField(blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Optional foreign keys for context
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    meeting = models.ForeignKey('meetings.Meeting', on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.template_type} to {self.recipient} - {self.status}"