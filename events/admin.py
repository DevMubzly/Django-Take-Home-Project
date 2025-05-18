from django.contrib import admin
from .models import EventCategory, Event, EventRegistration

class EventInline(admin.TabularInline):
    model = Event
    extra = 1
    fields = ('title', 'location', 'start_date', 'end_date', 'status')

class EventRegistrationInline(admin.TabularInline):
    model = EventRegistration
    extra = 1
    fields = ('user', 'attendance_status')

@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name', 'description')
    inlines = [EventInline]

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'location', 'start_date', 'end_date', 'status')
    list_filter = ('category', 'status', 'department')
    search_fields = ('title', 'description', 'location')
    list_editable = ('status',)
    inlines = [EventRegistrationInline]
    fieldsets = (
        ('Event Information', {
            'fields': ('title', 'description', 'category', 'department')
        }),
        ('Location and Time', {
            'fields': ('location', 'start_date', 'end_date', 'registration_deadline')
        }),
        ('Capacity and Status', {
            'fields': ('max_participants', 'status', 'organizer')
        }),
    )

@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'registration_date', 'attendance_status')
    list_filter = ('attendance_status', 'registration_date')
    search_fields = ('event__title', 'user__username', 'user__first_name', 'user__last_name')
    list_editable = ('attendance_status',)
