from django import forms
from .models import ContactMessage, RestaurantReservation, ConferenceBooking, CateringInquiry


class ContactForm(forms.ModelForm):
    """Contact form for general inquiries"""
    
    class Meta:
        model = ContactMessage
        fields = ['first_name', 'last_name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First Name',
                'required': True
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last Name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email Address',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone Number (optional)'
            }),
            'subject': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Your Message',
                'rows': 5,
                'required': True
            }),
        }


class RestaurantReservationForm(forms.ModelForm):
    """Restaurant table reservation form"""
    
    class Meta:
        model = RestaurantReservation
        fields = ['name', 'email', 'phone', 'date', 'meal_time', 'time', 'guests', 'special_requests']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Full Name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email Address',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone Number',
                'required': True
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True
            }),
            'meal_time': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time',
                'required': True
            }),
            'guests': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Number of Guests',
                'min': 1,
                'max': 50,
                'required': True
            }),
            'special_requests': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Dietary requirements, special occasions, seating preferences...',
                'rows': 3
            }),
        }


class ConferenceBookingForm(forms.ModelForm):
    """Conference room booking form"""
    
    class Meta:
        model = ConferenceBooking
        fields = [
            'organization_name', 'contact_person', 'email', 'phone',
            'event_type', 'event_date', 'end_date', 'start_time', 'end_time',
            'attendees', 'package', 'seating_arrangement',
            'catering_required', 'av_equipment_required', 'additional_requirements'
        ]
        widgets = {
            'organization_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Organization/Company Name',
                'required': True
            }),
            'contact_person': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contact Person Name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email Address',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone Number',
                'required': True
            }),
            'event_type': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'event_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'start_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time',
                'required': True
            }),
            'end_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time',
                'required': True
            }),
            'attendees': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Expected Attendees',
                'min': 1,
                'required': True
            }),
            'package': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'seating_arrangement': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'catering_required': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'av_equipment_required': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'additional_requirements': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Any additional requirements or special requests...',
                'rows': 3
            }),
        }


class CateringInquiryForm(forms.ModelForm):
    """Outside catering inquiry form"""
    
    class Meta:
        model = CateringInquiry
        fields = [
            'name', 'email', 'phone', 'event_type', 'event_date', 'event_time',
            'venue_address', 'guest_count', 'service_type', 'menu_preferences',
            'budget_range', 'additional_services'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email Address',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone Number',
                'required': True
            }),
            'event_type': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'event_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True
            }),
            'event_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time',
                'required': True
            }),
            'venue_address': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Event venue address/location',
                'rows': 2,
                'required': True
            }),
            'guest_count': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Expected Number of Guests',
                'min': 1,
                'required': True
            }),
            'service_type': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'menu_preferences': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Menu preferences, dietary requirements, specific dishes...',
                'rows': 3
            }),
            'budget_range': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Approximate budget (e.g., KES 50,000 - 100,000)'
            }),
            'additional_services': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Decorations, tent, chairs, serving equipment, etc.',
                'rows': 3
            }),
        }
