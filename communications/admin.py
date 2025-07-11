from django.contrib import admin
from .models import EmailTemplate, EmailLog

@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'template_type', 'subject', 'is_active', 'updated_at')
    list_filter = ('template_type', 'is_active', 'created_at')
    search_fields = ('name', 'subject')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'template_type', 'is_active')
        }),
        ('Email Content', {
            'fields': ('subject', 'html_content', 'text_content')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'template_type', 'subject', 'status', 'sent_at', 'created_at')
    list_filter = ('status', 'template_type', 'created_at')
    search_fields = ('recipient', 'subject')
    readonly_fields = ('created_at', 'sent_at')
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Email Information', {
            'fields': ('recipient', 'subject', 'template_type', 'status')
        }),
        ('Related Objects', {
            'fields': ('user', 'meeting')
        }),
        ('Error Information', {
            'fields': ('error_message',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'sent_at')
        }),
    )