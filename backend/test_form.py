#!/usr/bin/env python
"""Test the restaurant reservation form submission"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elleden.settings')
sys.path.insert(0, os.getcwd())

django.setup()

from pages.models import RestaurantReservation
from pages.forms import RestaurantReservationForm
from datetime import date, time
from django.test import RequestFactory

# Test 1: Direct model creation
print("=" * 60)
print("TEST 1: Direct Model Creation")
print("=" * 60)
try:
    res = RestaurantReservation.objects.create(
        name='Test User via Model',
        email='test@example.com',
        phone='254701234567',
        date=date(2025, 4, 26),
        meal_time='dinner',
        time=time(19, 0),
        guests=4,
        special_requests='Test'
    )
    print(f'[PASS] Reservation created')
    print(f'  Reference: {res.booking_reference}')
    print(f'  Price per person: {res.price_per_person}')
    print(f'  Total amount: {res.total_amount}')
    print(f'  Payment status: {res.payment_status}')
    res.delete()  # Clean up
except Exception as e:
    print(f'[FAIL] {type(e).__name__}: {e}')

# Test 2: Form submission
print("\n" + "=" * 60)
print("TEST 2: Form Submission")
print("=" * 60)
try:
    form_data = {
        'name': 'Test User via Form',
        'email': 'testform@example.com',
        'phone': '254701234567',
        'date': '2025-04-26',
        'meal_time': 'dinner',
        'time': '19:00',
        'guests': 4,
        'special_requests': 'Test'
    }
    form = RestaurantReservationForm(form_data)
    if form.is_valid():
        reservation = form.save()
        print(f'[PASS] Form submission successful')
        print(f'  Reference: {reservation.booking_reference}')
        print(f'  Price per person: {reservation.price_per_person}')
        print(f'  Total amount: {reservation.total_amount}')
        print(f'  Payment status: {reservation.payment_status}')
        reservation.delete()  # Clean up
    else:
        print(f'[FAIL] Form errors: {form.errors}')
except Exception as e:
    print(f'[FAIL] {type(e).__name__}: {e}')
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)
