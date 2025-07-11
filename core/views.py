from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import timedelta
from meetings.models import Meeting, MeetingAttendance
from groups.models import Group, GroupMembership
# from payments.models import Payment  # Uncomment when you add payments

def home(request):
    upcoming_meetings = Meeting.objects.filter(
        status='published',
        start_datetime__gte=timezone.now()
    ).order_by('start_datetime')[:3]
    
    context = {
        'upcoming_meetings': upcoming_meetings,
    }
    return render(request, 'core/home.html', context)

@login_required
def dashboard(request):
    """Enhanced dashboard with membership, events, and financial info"""
    user = request.user
    now = timezone.now()
    
    # === MEMBERSHIP INFO ===
    membership_info = {
        'status': 'Premium Member' if user.is_premium_member else 'Standard Member',
        'member_since': user.date_joined,
        'membership_expires': user.membership_end_date,
        'days_as_member': (now.date() - user.date_joined.date()).days,
    }
    
    # === MEETINGS/EVENTS INFO ===
    # User's upcoming meetings
    upcoming_meetings = Meeting.objects.filter(
        attendances__user=user,
        attendances__status='registered',
        start_datetime__gte=now
    ).order_by('start_datetime')[:5]
    
    # User's past meetings
    past_meetings = Meeting.objects.filter(
        attendances__user=user,
        attendances__status__in=['registered', 'attended'],
        start_datetime__lt=now
    ).order_by('-start_datetime')[:3]
    
    # Meeting stats
    total_meetings_attended = MeetingAttendance.objects.filter(
        user=user,
        status__in=['registered', 'attended']
    ).count()
    
    meetings_this_month = MeetingAttendance.objects.filter(
        user=user,
        status__in=['registered', 'attended'],
        registered_at__gte=now.replace(day=1)
    ).count()
    
    # === GROUP INFO ===
    user_groups = Group.objects.filter(
        memberships__user=user,
        memberships__is_active=True
    )[:5]
    
    groups_admin = GroupMembership.objects.filter(
        user=user,
        role='admin',
        is_active=True
    ).count()
    
    # === FINANCIAL INFO ===
    # TODO: Uncomment when you add payment system
    # total_spent = Payment.objects.filter(
    #     user=user,
    #     status='completed'
    # ).aggregate(total=Sum('amount'))['total'] or 0
    
    # payments_this_year = Payment.objects.filter(
    #     user=user,
    #     status='completed',
    #     created_at__year=now.year
    # ).aggregate(total=Sum('amount'))['total'] or 0
    
    # For now, mock financial data
    total_spent = 245.00  # Mock data
    payments_this_year = 125.00  # Mock data
    
    # === ADMIN STATS (if user is staff) ===
    admin_stats = {}
    if user.is_staff:
        admin_stats = {
            'total_members': user._meta.model.objects.filter(is_active=True).count(),
            'new_members_this_month': user._meta.model.objects.filter(
                date_joined__gte=now.replace(day=1)
            ).count(),
            'upcoming_meetings_count': Meeting.objects.filter(
                status='published',
                start_datetime__gte=now
            ).count(),
            'total_groups': Group.objects.count(),
        }
    
    # === RECENT ACTIVITY ===
    recent_registrations = MeetingAttendance.objects.filter(
        user=user
    ).order_by('-registered_at')[:3]
    
    context = {
        'membership_info': membership_info,
        'upcoming_meetings': upcoming_meetings,
        'past_meetings': past_meetings,
        'total_meetings_attended': total_meetings_attended,
        'meetings_this_month': meetings_this_month,
        'user_groups': user_groups,
        'groups_admin': groups_admin,
        'total_spent': total_spent,
        'payments_this_year': payments_this_year,
        'admin_stats': admin_stats,
        'recent_registrations': recent_registrations,
    }
    
    return render(request, 'core/dashboard.html', context)