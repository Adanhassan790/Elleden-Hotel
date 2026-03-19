from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
import logging

from .models import Booking, Payment, MpesaTransaction
from .forms import BookingForm, GuestBookingForm, PaymentForm
from .emails import send_booking_confirmation
from .mpesa import MpesaClient, MpesaError, process_mpesa_callback
from rooms.models import Room, RoomType

logger = logging.getLogger(__name__)


class BookingCreateView(CreateView):
    """Public booking form for website visitors"""
    model = Booking
    form_class = GuestBookingForm
    template_name = 'bookings/booking_form.html'
    
    def form_valid(self, form):
        room_type = form.cleaned_data['room_type']
        check_in = form.cleaned_data['check_in_date']
        check_out = form.cleaned_data['check_out_date']
        
        # Find available room of this type
        available_room = Room.objects.filter(
            room_type=room_type,
            status='available',
            is_active=True
        ).exclude(
            bookings__check_in_date__lt=check_out,
            bookings__check_out_date__gt=check_in,
            bookings__status__in=['confirmed', 'checked_in']
        ).first()
        
        if not available_room:
            messages.error(self.request, 'Sorry, no rooms of this type are available for the selected dates.')
            return self.form_invalid(form)
        
        booking = form.save(commit=False)
        booking.room = available_room
        booking.nightly_rate = room_type.base_price
        
        # If user is logged in, associate the booking
        if self.request.user.is_authenticated:
            booking.guest = self.request.user
        
        booking.save()
        
        # Send SMS and email confirmation
        send_booking_confirmation(booking)
        
        messages.success(self.request, f'Booking submitted successfully! Your reference: {booking.booking_reference}. Please proceed to payment.')
        # Redirect directly to payment instead of confirmation
        return redirect('bookings:payment', pk=booking.pk)


class BookingConfirmationView(DetailView):
    model = Booking
    template_name = 'bookings/booking_confirmation.html'
    context_object_name = 'booking'


class CustomerBookingListView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'bookings/customer_bookings.html'
    context_object_name = 'bookings'
    
    def get_queryset(self):
        return Booking.objects.filter(guest=self.request.user)


class CustomerBookingDetailView(LoginRequiredMixin, DetailView):
    model = Booking
    template_name = 'bookings/customer_booking_detail.html'
    context_object_name = 'booking'
    
    def get_queryset(self):
        return Booking.objects.filter(guest=self.request.user)


@login_required
def cancel_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk, guest=request.user)
    
    if booking.status in ['pending', 'confirmed']:
        booking.cancel()
        messages.success(request, 'Your booking has been cancelled.')
    else:
        messages.error(request, 'This booking cannot be cancelled.')
    
    return redirect('bookings:customer_list')


def check_availability(request):
    """API-style view to check room availability"""
    room_type_id = request.GET.get('room_type')
    check_in = request.GET.get('check_in')
    check_out = request.GET.get('check_out')
    
    if not all([room_type_id, check_in, check_out]):
        return render(request, 'bookings/availability_result.html', {
            'available': False,
            'message': 'Please provide all required information'
        })
    
    try:
        room_type = RoomType.objects.get(pk=room_type_id, is_active=True)
    except RoomType.DoesNotExist:
        return render(request, 'bookings/availability_result.html', {
            'available': False,
            'message': 'Invalid room type'
        })
    
    available_rooms = Room.objects.filter(
        room_type=room_type,
        status='available',
        is_active=True
    ).exclude(
        bookings__check_in_date__lt=check_out,
        bookings__check_out_date__gt=check_in,
        bookings__status__in=['confirmed', 'checked_in']
    )
    
    return render(request, 'bookings/availability_result.html', {
        'available': available_rooms.exists(),
        'room_type': room_type,
        'count': available_rooms.count()
    })


# ============ M-PESA PAYMENT VIEWS ============

def initiate_mpesa_payment(request, pk):
    """
    Initiate M-Pesa STK Push payment for a booking
    """
    booking = get_object_or_404(Booking, pk=pk)
    
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number', booking.guest_phone)
        amount = request.POST.get('amount', booking.balance_due)
        
        try:
            amount = int(float(amount))
        except (ValueError, TypeError):
            messages.error(request, 'Invalid amount specified.')
            return redirect('bookings:payment', pk=pk)
        
        if amount < 1:
            messages.error(request, 'Amount must be at least KES 1.')
            return redirect('bookings:payment', pk=pk)
        
        if amount > booking.balance_due:
            amount = int(booking.balance_due)
        
        try:
            mpesa = MpesaClient()
            response = mpesa.stk_push(
                phone_number=phone_number,
                amount=amount,
                account_reference=booking.booking_reference,
                transaction_desc='Hotel Booking'
            )
            
            if response.get('success'):
                # Save the transaction
                MpesaTransaction.objects.create(
                    booking=booking,
                    phone_number=phone_number,
                    amount=amount,
                    merchant_request_id=response.get('merchant_request_id', ''),
                    checkout_request_id=response.get('checkout_request_id'),
                    status='pending'
                )
                
                messages.info(
                    request, 
                    'Payment request sent! Please check your phone and enter your M-Pesa PIN to complete payment.'
                )
                return redirect('bookings:payment_status', pk=pk, checkout_id=response.get('checkout_request_id'))
            else:
                error_msg = response.get('error_message', 'Failed to initiate payment')
                messages.error(request, f'M-Pesa Error: {error_msg}')
                
        except MpesaError as e:
            logger.error(f'M-Pesa Error for booking {booking.booking_reference}: {str(e)}')
            messages.error(request, 'Unable to process M-Pesa payment. Please try again or contact support.')
        
        return redirect('bookings:payment', pk=pk)
    
    # GET request - show payment form
    return render(request, 'bookings/payment_form.html', {
        'booking': booking,
        'default_phone': booking.guest_phone,
        'amount_due': booking.balance_due
    })


def payment_status(request, pk, checkout_id):
    """
    Check M-Pesa payment status
    """
    booking = get_object_or_404(Booking, pk=pk)
    transaction = get_object_or_404(MpesaTransaction, checkout_request_id=checkout_id)
    
    return render(request, 'bookings/payment_status.html', {
        'booking': booking,
        'transaction': transaction,
        'checkout_id': checkout_id
    })


def check_payment_status(request, checkout_id):
    """
    AJAX endpoint to check M-Pesa payment status
    """
    try:
        transaction = MpesaTransaction.objects.get(checkout_request_id=checkout_id)
        
        if transaction.status == 'pending':
            # Query M-Pesa for status
            try:
                mpesa = MpesaClient()
                result = mpesa.query_stk_status(checkout_id)
                
                result_code = result.get('ResultCode')
                if result_code is not None:
                    if result_code == 0:
                        # Payment successful - this shouldn't happen here as callback should handle it
                        # But we'll handle it just in case
                        if transaction.status == 'pending':
                            receipt = result.get('MpesaReceiptNumber', '')
                            transaction.mark_completed(receipt, result.get('ResultDesc', ''))
                    elif result_code != 1032:  # 1032 means pending
                        transaction.mark_failed(result_code, result.get('ResultDesc', 'Payment failed'))
            except MpesaError:
                pass  # Continue with current status
        
        return JsonResponse({
            'status': transaction.status,
            'receipt': transaction.mpesa_receipt_number,
            'booking_status': transaction.booking.status,
            'payment_status': transaction.booking.payment_status,
            'amount_paid': str(transaction.booking.amount_paid),
            'balance_due': str(transaction.booking.balance_due)
        })
    except MpesaTransaction.DoesNotExist:
        return JsonResponse({'error': 'Transaction not found'}, status=404)


@csrf_exempt
@require_POST
def mpesa_callback(request):
    """
    Callback URL for M-Pesa STK Push results
    This endpoint receives payment confirmations from Safaricom
    """
    try:
        callback_data = json.loads(request.body.decode('utf-8'))
        logger.info(f'M-Pesa Callback received: {json.dumps(callback_data)}')
        
        result = process_mpesa_callback(callback_data)
        
        checkout_request_id = result.get('checkout_request_id')
        if not checkout_request_id:
            logger.error('No checkout_request_id in callback')
            return JsonResponse({'ResultCode': 0, 'ResultDesc': 'Accepted'})
        
        try:
            transaction = MpesaTransaction.objects.get(checkout_request_id=checkout_request_id)
            
            if result.get('success'):
                mpesa_receipt = result.get('mpesa_receipt', '')
                transaction.mark_completed(mpesa_receipt, result.get('result_desc', ''))
                logger.info(f'Payment completed for booking {transaction.booking.booking_reference}: {mpesa_receipt}')
            else:
                transaction.mark_failed(
                    result.get('result_code', -1),
                    result.get('result_desc', 'Payment failed or cancelled')
                )
                logger.info(f'Payment failed for booking {transaction.booking.booking_reference}: {result.get("result_desc")}')
                
        except MpesaTransaction.DoesNotExist:
            logger.error(f'Transaction not found for checkout_request_id: {checkout_request_id}')
        
        # Always return success to M-Pesa
        return JsonResponse({'ResultCode': 0, 'ResultDesc': 'Accepted'})
        
    except json.JSONDecodeError:
        logger.error('Invalid JSON in M-Pesa callback')
        return JsonResponse({'ResultCode': 0, 'ResultDesc': 'Accepted'})
    except Exception as e:
        logger.error(f'Error processing M-Pesa callback: {str(e)}')
        return JsonResponse({'ResultCode': 0, 'ResultDesc': 'Accepted'})
