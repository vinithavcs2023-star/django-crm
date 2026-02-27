from django.contrib import admin
from .models import Record, CallHistory, Email, Task

class CallHistoryInline(admin.TabularInline):
    model = CallHistory
    extra = 1

class EmailInline(admin.TabularInline):
    model = Email
    extra = 1

class TaskInline(admin.TabularInline):
    model = Task
    extra = 1

class RecordAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'customer_type', 'is_active', 'last_contacted')
    list_filter = ('is_active', 'customer_type', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'phone', 'company')
    inlines = [CallHistoryInline, EmailInline, TaskInline]
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Address Information', {
            'fields': ('address', 'city', 'state', 'zipcode')
        }),
        ('Professional Information', {
            'fields': ('company', 'job_title', 'customer_type')
        }),
        ('Status & Notes', {
            'fields': ('is_active', 'notes', 'last_contacted')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')

class CallHistoryAdmin(admin.ModelAdmin):
    list_display = ('record', 'call_type', 'duration_seconds', 'called_at')
    list_filter = ('call_type', 'called_at')
    search_fields = ('record__first_name', 'record__last_name')

class EmailAdmin(admin.ModelAdmin):
    list_display = ('record', 'subject', 'sent_at')
    list_filter = ('sent_at',)
    search_fields = ('record__first_name', 'record__last_name', 'subject')

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'record', 'due_date', 'status')
    list_filter = ('status', 'due_date')
    search_fields = ('title', 'record__first_name', 'record__last_name')

admin.site.register(Record, RecordAdmin)
admin.site.register(CallHistory, CallHistoryAdmin)
admin.site.register(Email, EmailAdmin)
admin.site.register(Task, TaskAdmin)