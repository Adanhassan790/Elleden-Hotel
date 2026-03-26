from django.contrib import admin
from .models import Booking, Payment


class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0
    readonly_fields = ('created_at',)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_reference', 'guest_name', 'room', 'check_in_date', 
                    'check_out_date', 'status', 'payment_status', 'total_amount')
    list_filter = ('status', 'payment_status', 'room__room_type', 'check_in_date')
    search_fields = ('booking_reference', 'guest_name', 'guest_email', 'guest_phone')
    readonly_fields = ('booking_reference', 'total_nights', 'subtotal', 'total_amount', 
                       'created_at', 'updated_at')
    date_hierarchy = 'check_in_date'
    inlines = [PaymentInline]
    
    fieldsets = (
        ('Booking Info', {
            'fields': ('booking_reference', 'status', 'payment_status')
        }),
        ('Guest Details', {
            'fields': ('guest', 'guest_name', 'guest_email', 'guest_phone', 
                      'guest_id_number', 'guest_nationality')
        }),
        ('Room & Dates', {
            'fields': ('room', 'room_type', 'check_in_date', 'check_out_date',
                      'actual_check_in', 'actual_check_out', 'adults', 'children')
        }),
        ('Pricing', {
            'fields': ('nightly_rate', 'total_nights', 'subtotal', 'discount', 
                      'tax', 'total_amount', 'amount_paid')
        }),
        ('Notes', {
            'fields': ('special_requests', 'internal_notes'),
            'classes': ('collapse',)
        }),
        ('Tracking', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['confirm_bookings', 'cancel_bookings']
    
    def confirm_bookings(self, request, queryset):
        for booking in queryset.filter(status='pending'):
            booking.confirm()
        self.message_user(request, 'Selected bookings have been confirmed.')
    confirm_bookings.short_description = 'Confirm selected bookings'
    
    def cancel_bookings(self, request, queryset):
        for booking in queryset.exclude(status__in=['checked_in', 'checked_out', 'cancelled']):
            booking.cancel()
        self.message_user(request, 'Selected bookings have been cancelled.')
    cancel_bookings.short_description = 'Cancel selected bookings'


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('booking', 'amount', 'payment_method', 'transaction_reference', 'created_at')
    list_filter = ('payment_method', 'created_at')
    search_fields = ('booking__booking_reference', 'transaction_reference')
    readonly_fields = ('created_at',)
