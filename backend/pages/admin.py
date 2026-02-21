from django.contrib import admin
from .models import ContactMessage, RestaurantReservation, ConferenceBooking, CateringInquiry


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'subject', 'status', 'created_at']
    list_filter = ['status', 'subject', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'message']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['status']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Message Details', {
            'fields': ('subject', 'message', 'status')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(RestaurantReservation)
class RestaurantReservationAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'date', 'meal_time', 'time', 'guests', 'status', 'created_at']
    list_filter = ['status', 'meal_time', 'date', 'created_at']
    search_fields = ['name', 'email', 'phone']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['status']
    ordering = ['-date', '-time']
    date_hierarchy = 'date'
    
    fieldsets = (
        ('Guest Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Reservation Details', {
            'fields': ('date', 'meal_time', 'time', 'guests', 'special_requests')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ConferenceBooking)
class ConferenceBookingAdmin(admin.ModelAdmin):
    list_display = ['organization_name', 'contact_person', 'event_type', 'event_date', 'attendees', 'package', 'status', 'created_at']
    list_filter = ['status', 'event_type', 'package', 'event_date', 'created_at']
    search_fields = ['organization_name', 'contact_person', 'email', 'phone']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['status']
    ordering = ['-event_date']
    date_hierarchy = 'event_date'
    
    fieldsets = (
        ('Organization Details', {
            'fields': ('organization_name', 'contact_person', 'email', 'phone')
        }),
        ('Event Details', {
            'fields': ('event_type', 'event_date', 'end_date', 'start_time', 'end_time', 'attendees')
        }),
        ('Package & Setup', {
            'fields': ('package', 'seating_arrangement', 'catering_required', 'av_equipment_required')
        }),
        ('Additional Information', {
            'fields': ('additional_requirements',)
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(CateringInquiry)
class CateringInquiryAdmin(admin.ModelAdmin):
    list_display = ['name', 'event_type', 'event_date', 'guest_count', 'service_type', 'status', 'created_at']
    list_filter = ['status', 'event_type', 'service_type', 'event_date', 'created_at']
    search_fields = ['name', 'email', 'phone', 'venue_address']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['status']
    ordering = ['-event_date']
    date_hierarchy = 'event_date'
    
    fieldsets = (
        ('Client Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Event Details', {
            'fields': ('event_type', 'event_date', 'event_time', 'venue_address', 'guest_count')
        }),
        ('Catering Requirements', {
            'fields': ('service_type', 'menu_preferences', 'budget_range', 'additional_services')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
