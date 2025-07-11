from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Meeting, MeetingAttendance
from groups.models import Group

def meeting_list(request):
    """Public meeting list - shows upcoming published meetings"""
    # Get filter parameters
    meeting_type = request.GET.get('type', '')
    group_id = request.GET.get('group', '')
    search = request.GET.get('search', '')
    
    # Base queryset - upcoming published meetings
    meetings = Meeting.objects.filter(
        status='published',
        start_datetime__gte=timezone.now()
    ).select_related('created_by', 'group').prefetch_related('attendances')
    
    # Apply filters
    if meeting_type:
        meetings = meetings.filter(meeting_type=meeting_type)
    
    if group_id:
        meetings = meetings.filter(group_id=group_id)
    
    if search:
        meetings = meetings.filter(
            Q(title__icontains=search) | 
            Q(description__icontains=search)
        )
    
    # Order by date
    meetings = meetings.order_by('start_datetime')
    
    # Get filter options
    groups = Group.objects.all()
    meeting_types = Meeting.MEETING_TYPES
    
    context = {
        'meetings': meetings,
        'groups': groups,
        'meeting_types': meeting_types,
        'current_type': meeting_type,
        'current_group': group_id,
        'search_query': search,
    }
    return render(request, 'meetings/meeting_list.html', context)

def meeting_detail(request, slug):
    """Meeting detail page with registration option"""
    meeting = get_object_or_404(Meeting, slug=slug, status='published')
    
    # Check if user is already registered
    user_registered = False
    user_attendance = None
    if request.user.is_authenticated:
        try:
            user_attendance = MeetingAttendance.objects.get(
                meeting=meeting, 
                user=request.user
            )
            user_registered = user_attendance.status == 'registered'
        except MeetingAttendance.DoesNotExist:
            pass
    
    # Get attendees (for public display)
    attendees = MeetingAttendance.objects.filter(
        meeting=meeting,
        status='registered'
    ).select_related('user')[:10]  # Show first 10
    
    # Check if meeting is full
    is_full = False
    if meeting.max_attendees:
        current_attendees = attendees.count()
        is_full = current_attendees >= meeting.max_attendees
    
    context = {
        'meeting': meeting,
        'user_registered': user_registered,
        'user_attendance': user_attendance,
        'attendees': attendees,
        'attendee_count': meeting.attendee_count,
        'is_full': is_full,
        'can_register': (
            request.user.is_authenticated and 
            not user_registered and 
            not is_full and
            meeting.start_datetime > timezone.now()
        )
    }
    return render(request, 'meetings/meeting_detail.html', context)

@login_required
@require_POST
def register_for_meeting(request, slug):
    """Register user for a meeting"""
    meeting = get_object_or_404(Meeting, slug=slug, status='published')
    
    # Check if meeting is in the future
    if meeting.start_datetime <= timezone.now():
        messages.error(request, 'Cannot register for past meetings.')
        return redirect('meetings:detail', slug=slug)
    
    # Check if meeting is full
    if meeting.max_attendees and meeting.attendee_count >= meeting.max_attendees:
        messages.error(request, 'This meeting is full.')
        return redirect('meetings:detail', slug=slug)
    
    # Check if user is already registered
    attendance, created = MeetingAttendance.objects.get_or_create(
        meeting=meeting,
        user=request.user,
        defaults={
            'status': 'registered',
            'payment_required': meeting.price > 0,
            'payment_completed': meeting.price == 0,  # Free meetings don't need payment
        }
    )
    
    if created:
        messages.success(request, f'Successfully registered for "{meeting.title}"!')
        
        # If payment is required, redirect to payment (we'll add this later)
        if meeting.price > 0:
            messages.info(request, f'Payment of ${meeting.price} is required to complete registration.')
    else:
        if attendance.status == 'cancelled':
            # Reactivate cancelled registration
            attendance.status = 'registered'
            attendance.save()
            messages.success(request, f'Successfully re-registered for "{meeting.title}"!')
        else:
            messages.info(request, 'You are already registered for this meeting.')
    
    return redirect('meetings:detail', slug=slug)

@login_required
@require_POST
def cancel_meeting_registration(request, slug):
    """Cancel user's meeting registration"""
    meeting = get_object_or_404(Meeting, slug=slug)
    
    try:
        attendance = MeetingAttendance.objects.get(
            meeting=meeting,
            user=request.user
        )
        attendance.status = 'cancelled'
        attendance.save()
        messages.success(request, f'Registration cancelled for "{meeting.title}".')
    except MeetingAttendance.DoesNotExist:
        messages.error(request, 'You are not registered for this meeting.')
    
    return redirect('meetings:detail', slug=slug)

@login_required
def my_meetings(request):
    """User's personal meeting dashboard"""
    # Upcoming meetings user is registered for
    upcoming_meetings = Meeting.objects.filter(
        attendances__user=request.user,
        attendances__status='registered',
        start_datetime__gte=timezone.now()
    ).order_by('start_datetime')
    
    # Past meetings user attended
    past_meetings = Meeting.objects.filter(
        attendances__user=request.user,
        attendances__status__in=['registered', 'attended'],
        start_datetime__lt=timezone.now()
    ).order_by('-start_datetime')[:5]  # Last 5
    
    context = {
        'upcoming_meetings': upcoming_meetings,
        'past_meetings': past_meetings,
    }
    return render(request, 'meetings/my_meetings.html', context)