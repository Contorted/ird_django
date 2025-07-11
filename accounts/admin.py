from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import CustomUser, MemberProfile

class MemberProfileInline(admin.StackedInline):
    model = MemberProfile
    can_delete = False
    verbose_name_plural = 'Profile Information'

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    inlines = (MemberProfileInline,)
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_premium_member', 'is_staff', 'created_at')
    list_filter = ('is_premium_member', 'is_staff', 'is_superuser', 'is_active', 'created_at')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('-created_at',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Information', {
            'fields': ('phone', 'date_of_birth', 'bio', 'profile_picture')
        }),
        ('Membership Information', {
            'fields': ('is_premium_member', 'membership_start_date', 'membership_end_date')
        }),
    )

@admin.register(MemberProfile)
class MemberProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'company', 'position', 'created_at')
    list_filter = ('company', 'created_at')
    search_fields = ('user__email', 'user__username', 'company', 'position')