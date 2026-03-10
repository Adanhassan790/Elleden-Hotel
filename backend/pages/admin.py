from django.contrib import admin
from .models import (ContactMessage, RestaurantReservation, ConferenceBooking, 
                     CateringInquiry, CateringPackage, CateringOrder, 
                     ServicePayment, ServiceMpesaTransaction)


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
    list_display = ['booking_reference', 'name', 'email', 'phone', 'date', 'meal_time', 'time', 'guests', 'status', 'created_at']
    list_filter = ['status', 'meal_time', 'date', 'created_at']
    search_fields = ['booking_reference', 'name', 'email', 'phone']
    readonly_fields = ['booking_reference', 'created_at', 'updated_at']
    list_editable = ['status']
    ordering = ['-date', '-time']
    date_hierarchy = 'date'
    
    fieldsets = (
        ('Booking Reference', {
            'fields': ('booking_reference',)
        }),
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
    list_display = ['booking_reference', 'organization_name', 'contact_person', 'event_type', 
                   'event_date', 'attendees', 'package', 'total_amount', 'payment_status', 'status', 'created_at']
    list_filter = ['status', 'payment_status', 'event_type', 'package', 'event_date', 'created_at']
    search_fields = ['booking_reference', 'organization_name', 'contact_person', 'email', 'phone']
    readonly_fields = ['booking_reference', 'base_price', 'catering_cost', 'equipment_cost', 'total_amount', 'created_at', 'updated_at']
    list_editable = ['status', 'payment_status']
    ordering = ['-event_date']
    date_hierarchy = 'event_date'
    
    fieldsets = (
        ('Booking Reference', {
            'fields': ('booking_reference',)
        }),
        ('Organization Details', {
            'fields': ('organization_name', 'contact_person', 'email', 'phone')
        }),
        ('Event Details', {
            'fields': ('event_type', 'event_date', 'end_date', 'start_time', 'end_time', 'attendees')
        }),
        ('Package & Setup', {
            'fields': ('package', 'seating_arrangement', 'catering_required', 'av_equipment_required')
        }),
        ('Pricing', {
            'fields': ('base_price', 'catering_cost', 'equipment_cost', 'total_amount', 'amount_paid')
        }),
        ('Additional Information', {
            'fields': ('additional_requirements',)
        }),
        ('Status', {
            'fields': ('status', 'payment_status')
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


@admin.register(CateringPackage)
class CateringPackageAdmin(admin.ModelAdmin):
    list_display = ['name', 'price_per_person', 'minimum_guests', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    list_editable = ['is_active', 'price_per_person']


@admin.register(CateringOrder)
class CateringOrderAdmin(admin.ModelAdmin):
    list_display = ['booking_reference', 'name', 'event_type', 'event_date', 'guest_count', 
                   'package', 'total_amount', 'payment_status', 'status', 'created_at']
    list_filter = ['status', 'payment_status', 'event_type', 'event_date', 'created_at']
    search_fields = ['booking_reference', 'name', 'email', 'phone', 'venue_address']
    readonly_fields = ['booking_reference', 'total_amount', 'created_at', 'updated_at']
    list_editable = ['status', 'payment_status']
    ordering = ['-event_date']
    date_hierarchy = 'event_date'
    
    fieldsets = (
        ('Booking Reference', {
            'fields': ('booking_reference',)
        }),
        ('Client Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Event Details', {
            'fields': ('event_type', 'event_date', 'event_time', 'venue_address', 'guest_count')
        }),
        ('Package & Menu', {
            'fields': ('package', 'custom_menu', 'special_requests')
        }),
        ('Pricing', {
            'fields': ('price_per_person', 'delivery_fee', 'total_amount', 'amount_paid')
        }),
        ('Status', {
            'fields': ('status', 'payment_status')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ServicePayment)
class ServicePaymentAdmin(admin.ModelAdmin):
    list_display = ['service_type', 'conference_booking', 'catering_order', 'amount', 
                   'payment_method', 'transaction_reference', 'created_at']
    list_filter = ['service_type', 'payment_method', 'created_at']
    search_fields = ['transaction_reference']
    readonly_fields = ['created_at']
    ordering = ['-created_at']


@admin.register(ServiceMpesaTransaction)
class ServiceMpesaTransactionAdmin(admin.ModelAdmin):
    list_display = ['service_type', 'conference_booking', 'catering_order', 'checkout_request_id', 
                   'amount', 'phone_number', 'mpesa_receipt_number', 'status', 'created_at']
    list_filter = ['service_type', 'status', 'created_at']
    search_fields = ['checkout_request_id', 'mpesa_receipt_number', 'phone_number']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
