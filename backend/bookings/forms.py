from django import forms
from django.utils import timezone
from .models import Booking, Payment
from rooms.models import Room, RoomType


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['guest_name', 'guest_email', 'guest_phone', 'guest_id_number',
                  'guest_nationality', 'room_type', 'check_in_date', 'check_out_date',
                  'adults', 'children', 'special_requests']
        widgets = {
            'check_in_date': forms.DateInput(attrs={'type': 'date'}),
            'check_out_date': forms.DateInput(attrs={'type': 'date'}),
            'special_requests': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in_date')
        check_out = cleaned_data.get('check_out_date')
        
        if check_in and check_out:
            if check_in < timezone.now().date():
                raise forms.ValidationError('Check-in date cannot be in the past')
            if check_out <= check_in:
                raise forms.ValidationError('Check-out date must be after check-in date')
        
        return cleaned_data


class GuestBookingForm(forms.ModelForm):
    """Simplified form for guest bookings from the website"""
    room_type = forms.ModelChoiceField(
        queryset=RoomType.objects.filter(is_active=True),
        empty_label="Select Room Type"
    )
    
    class Meta:
        model = Booking
        fields = ['guest_name', 'guest_email', 'guest_phone', 'room_type',
                  'check_in_date', 'check_out_date', 'adults', 'children', 
                  'special_requests']
        widgets = {
            'check_in_date': forms.DateInput(attrs={'type': 'date', 'min': timezone.now().date().isoformat()}),
            'check_out_date': forms.DateInput(attrs={'type': 'date'}),
            'special_requests': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Any special requests or requirements...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        
        self.fields['guest_name'].widget.attrs['placeholder'] = 'Full Name'
        self.fields['guest_email'].widget.attrs['placeholder'] = 'Email Address'
        self.fields['guest_phone'].widget.attrs['placeholder'] = 'Phone Number'


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount', 'payment_method', 'transaction_reference', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
