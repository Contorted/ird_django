from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify
from groups.models import Group

class Meeting(models.Model):
    MEETING_TYPES = [
        ('online', 'Online'),
        ('in_person', 'In Person'),
        ('hybrid', 'Hybrid'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    
    title = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(unique=True, max_length=200, blank=True)
    description = models.TextField()
    meeting_type = models.CharField(max_length=20, choices=MEETING_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    start_datetime = models.DateTimeField(db_index=True)
    end_datetime = models.DateTimeField()
    location = models.CharField(max_length=200, blank=True)
    online_link = models.URLField(blank=True)
    max_attendees = models.PositiveIntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_members_only = models.BooleanField(default=False)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def is_upcoming(self):
        return self.start_datetime > timezone.now()

    @property
    def attendee_count(self):
        return self.attendances.filter(status='registered').count()

class MeetingAttendance(models.Model):
    STATUSES = [
        ('registered', 'Registered'),
        ('attended', 'Attended'),
        ('no_show', 'No Show'),
        ('cancelled', 'Cancelled'),
    ]
    
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name='attendances')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUSES, default='registered')
    registered_at = models.DateTimeField(auto_now_add=True)
    payment_required = models.BooleanField(default=False)
    payment_completed = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    
    class Meta:
        unique_together = ['meeting', 'user']

    def __str__(self):
        return f"{self.user.username} - {self.meeting.title}"