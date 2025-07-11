from django.core.management.base import BaseCommand
from communications.models import EmailTemplate

class Command(BaseCommand):
    help = 'Set up initial email templates for IRD'
    
    def handle(self, *args, **options):
        templates = [
            {
                'name': 'Welcome Email',
                'template_type': 'welcome',
                'subject': 'Welcome to the Institute of Roll Design (IRD)!',
                'html_content': '''
<!DOCTYPE html>
<html>
<head>
    <style>
        .email-container { max-width: 600px; margin: 0 auto; font-family: Arial, sans-serif; }
        .header { background-color: #0d6efd; color: white; padding: 20px; text-align: center; }
        .content { padding: 20px; }
        .footer { background-color: #f8f9fa; padding: 15px; text-align: center; font-size: 12px; color: #666; }
        .btn { display: inline-block; padding: 10px 20px; background-color: #0d6efd; color: white; text-decoration: none; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="email-container">
        <div class="header">
            <h1>Welcome to IRD!</h1>
        </div>
        <div class="content">
            <h2>Hello {{ user_name }},</h2>
            <p>Welcome to the Institute of Roll Design! We're excited to have you join our community of roll design professionals.</p>
            
            <p>As a member of IRD, you now have access to:</p>
            <ul>
                <li>Professional development workshops and courses</li>
                <li>Industry networking events and meetings</li>
                <li>Exclusive technical resources and research</li>
                <li>Connection with leading professionals in roll design</li>
            </ul>
            
            <p>Ready to get started?</p>
            <p><a href="{{ dashboard_url }}" class="btn">Go to Your Dashboard</a></p>
            
            <p>You can also:</p>
            <ul>
                <li><a href="{{ meetings_url }}">Browse upcoming meetings</a></li>
                <li><a href="{{ login_url }}">Login to your account</a></li>
            </ul>
            
            <p>If you have any questions, please don't hesitate to contact us.</p>
            
            <p>Best regards,<br>The IRD Team</p>
        </div>
        <div class="footer">
            <p>Institute of Roll Design | Advancing excellence in roll technology and design innovation</p>
        </div>
    </div>
</body>
</html>
                ''',
                'text_content': '''
Welcome to the Institute of Roll Design (IRD)!

Hello {{ user_name }},

Welcome to the Institute of Roll Design! We're excited to have you join our community of roll design professionals.

As a member of IRD, you now have access to:
- Professional development workshops and courses
- Industry networking events and meetings
- Exclusive technical resources and research
- Connection with leading professionals in roll design

Ready to get started? Visit your dashboard: {{ dashboard_url }}

You can also:
- Browse upcoming meetings: {{ meetings_url }}
- Login to your account: {{ login_url }}

If you have any questions, please don't hesitate to contact us.

Best regards,
The IRD Team

Institute of Roll Design | Advancing excellence in roll technology and design innovation
                '''
            },
            {
                'name': 'Meeting Registration Confirmation',
                'template_type': 'meeting_confirmation',
                'subject': 'Registration Confirmed: {{ meeting_title }}',
                'html_content': '''
<!DOCTYPE html>
<html>
<head>
    <style>
        .email-container { max-width: 600px; margin: 0 auto; font-family: Arial, sans-serif; }
        .header { background-color: #198754; color: white; padding: 20px; text-align: center; }
        .content { padding: 20px; }
        .meeting-details { background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 15px 0; }
        .footer { background-color: #f8f9fa; padding: 15px; text-align: center; font-size: 12px; color: #666; }
        .btn { display: inline-block; padding: 10px 20px; background-color: #198754; color: white; text-decoration: none; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="email-container">
        <div class="header">
            <h1>Registration Confirmed!</h1>
        </div>
        <div class="content">
            <h2>Hello {{ user_name }},</h2>
            <p>Your registration for <strong>{{ meeting_title }}</strong> has been confirmed!</p>
            
            <div class="meeting-details">
                <h3>Meeting Details:</h3>
                <p><strong>Title:</strong> {{ meeting_title }}</p>
                <p><strong>Date:</strong> {{ meeting_date }}</p>
                <p><strong>Time:</strong> {{ meeting_time }}</p>
                <p><strong>Type:</strong> {{ meeting_type }}</p>
                {% if meeting_location %}<p><strong>Location:</strong> {{ meeting_location }}</p>{% endif %}
                {% if meeting_link %}<p><strong>Online Link:</strong> <a href="{{ meeting_link }}">Join Meeting</a></p>{% endif %}
                <p><strong>Organizer:</strong> {{ organizer_name }}</p>
            </div>
            
            {% if meeting_description %}
            <h3>About This Meeting:</h3>
            <p>{{ meeting_description }}</p>
            {% endif %}
            
            <p>We'll send you a reminder 24 hours before the meeting.</p>
            
            <p><a href="{{ meeting_url }}" class="btn">View Meeting Details</a></p>
            
            <p>Looking forward to seeing you there!</p>
            
            <p>Best regards,<br>The IRD Team</p>
        </div>
        <div class="footer">
            <p>Institute of Roll Design | Professional Development Through Connection</p>
        </div>
    </div>
</body>
</html>
                ''',
                'text_content': '''
Registration Confirmed: {{ meeting_title }}

Hello {{ user_name }},

Your registration for {{ meeting_title }} has been confirmed!

Meeting Details:
- Title: {{ meeting_title }}
- Date: {{ meeting_date }}
- Time: {{ meeting_time }}
- Type: {{ meeting_type }}
{% if meeting_location %}- Location: {{ meeting_location }}{% endif %}
{% if meeting_link %}- Online Link: {{ meeting_link }}{% endif %}
- Organizer: {{ organizer_name }}

{% if meeting_description %}About This Meeting:
{{ meeting_description }}{% endif %}

We'll send you a reminder 24 hours before the meeting.

View meeting details: {{ meeting_url }}

Looking forward to seeing you there!

Best regards,
The IRD Team

Institute of Roll Design | Professional Development Through Connection
                '''
            },
            {
                'name': 'Meeting Reminder',
                'template_type': 'meeting_reminder',
                'subject': 'Reminder: {{ meeting_title }} is tomorrow!',
                'html_content': '''
<!DOCTYPE html>
<html>
<head>
    <style>
        .email-container { max-width: 600px; margin: 0 auto; font-family: Arial, sans-serif; }
        .header { background-color: #ffc107; color: #000; padding: 20px; text-align: center; }
        .content { padding: 20px; }
        .meeting-info { background-color: #fff3cd; padding: 15px; border-radius: 5px; margin: 15px 0; border-left: 4px solid #ffc107; }
        .footer { background-color: #f8f9fa; padding: 15px; text-align: center; font-size: 12px; color: #666; }
        .btn { display: inline-block; padding: 10px 20px; background-color: #ffc107; color: #000; text-decoration: none; border-radius: 5px; font-weight: bold; }
    </style>
</head>
<body>
    <div class="email-container">
        <div class="header">
            <h1>Meeting Reminder</h1>
        </div>
        <div class="content">
            <h2>Hello {{ user_name }},</h2>
            <p>This is a friendly reminder that you're registered for <strong>{{ meeting_title }}</strong> tomorrow!</p>
            
            <div class="meeting-info">
                <h3>📅 Meeting Information:</h3>
                <p><strong>Title:</strong> {{ meeting_title }}</p>
                <p><strong>Date:</strong> {{ meeting_date }}</p>
                <p><strong>Time:</strong> {{ meeting_time }}</p>
                <p><strong>Type:</strong> {{ meeting_type }}</p>
                {% if meeting_location %}<p><strong>Location:</strong> {{ meeting_location }}</p>{% endif %}
            </div>
            
            {% if meeting_link %}
            <p><strong>Online Meeting Link:</strong></p>
            <p><a href="{{ meeting_link }}" class="btn">Join Meeting</a></p>
            {% endif %}
            
            <p>Don't forget to:</p>
            <ul>
                <li>Mark your calendar</li>
                <li>Prepare any materials you might need</li>
                {% if meeting_type == 'Online' %}<li>Test your internet connection and audio/video</li>{% endif %}
                {% if meeting_type == 'In Person' %}<li>Plan your travel time to the venue</li>{% endif %}
            </ul>
            
            <p><a href="{{ meeting_url }}">View full meeting details</a></p>
            
            <p>See you there!</p>
            
            <p>Best regards,<br>The IRD Team</p>
        </div>
        <div class="footer">
            <p>Institute of Roll Design | Connecting Industry Professionals</p>
        </div>
    </div>
</body>
</html>
                ''',
                'text_content': '''
Meeting Reminder: {{ meeting_title }} is tomorrow!

Hello {{ user_name }},

This is a friendly reminder that you're registered for {{ meeting_title }} tomorrow!

Meeting Information:
- Title: {{ meeting_title }}
- Date: {{ meeting_date }}
- Time: {{ meeting_time }}
- Type: {{ meeting_type }}
{% if meeting_location %}- Location: {{ meeting_location }}{% endif %}

{% if meeting_link %}Online Meeting Link: {{ meeting_link }}{% endif %}

Don't forget to:
- Mark your calendar
- Prepare any materials you might need
{% if meeting_type == 'Online' %}- Test your internet connection and audio/video{% endif %}
{% if meeting_type == 'In Person' %}- Plan your travel time to the venue{% endif %}

View full meeting details: {{ meeting_url }}

See you there!

Best regards,
The IRD Team

Institute of Roll Design | Connecting Industry Professionals
                '''
            }
        ]
        
        for template_data in templates:
            template, created = EmailTemplate.objects.get_or_create(
                template_type=template_data['template_type'],
                defaults=template_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created email template: {template.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Email template already exists: {template.name}')
                )
        
        self.stdout.write(
            self.style.SUCCESS('Email template setup completed!')
        )