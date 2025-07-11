from django.contrib import admin
from .models import Meeting, MeetingAttendance

class MeetingAttendanceInline(admin.TabularInline):
    model = MeetingAttendance
    extra = 0

@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ('title', 'meeting_type', 'status', 'start_datetime', 'attendee_count', 'created_by')
    list_filter = ('meeting_type', 'status', 'is_members_only', 'start_datetime')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'start_datetime'
    inlines = [MeetingAttendanceInline]

@admin.register(MeetingAttendance)
class MeetingAttendanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'meeting', 'status', 'payment_completed', 'registered_at')
    list_filter = ('status', 'payment_completed', 'registered_at')
    search_fields = ('user__username', 'meeting__title')