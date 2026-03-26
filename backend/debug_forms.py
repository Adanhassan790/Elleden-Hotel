import requests
from datetime import datetime, timedelta
import re

def get_csrf_token(session, url):
    """Fetch a page and extract CSRF token"""
    response = session.get(url)
    if response.status_code != 200:
        return None
    match = re.search(r'<input[^>]*name=["\']csrfmiddlewaretoken["\'][^>]*value=["\']([^"\']+)["\']', response.text)
    return match.group(1) if match else None

session = requests.Session()

# Debug conference form
print("Testing Conference Form...")
csrf_token = get_csrf_token(session, "http://127.0.0.1:8000/conference/")

conference_data = {
    'organization_name': 'Tech Corp',
    'contact_person': 'Jane Smith',
    'email': 'jane@example.com',
    'phone': '254787654321',
    'event_type': 'conference',
    'event_date': (datetime.now() + timedelta(days=5)).strftime('%Y-%m-%d'),
    'end_date': (datetime.now() + timedelta(days=5)).strftime('%Y-%m-%d'),
    'start_time': '09:00',
    'end_time': '17:00',
    'attendees': 50,
    'package': '1',  # Try with ID instead of 'standard'
    'seating_arrangement': 'theater',
    'catering_required': False,
    'av_equipment_required': False,
    'csrfmiddlewaretoken': csrf_token
}

response = session.post("http://127.0.0.1:8000/conference/", data=conference_data, allow_redirects=False)

print(f"Status: {response.status_code}")
print(f"Response contains 'error': {'error' in response.text.lower()}")
print(f"Response contains 'required': {'required' in response.text.lower()}")

# Extract form errors from response
error_matches = re.findall(r'<div[^>]*class="form-error"[^>]*>([^<]+)</div>', response.text)
if error_matches:
    print(f"\nForm Errors Found:")
    for i, error in enumerate(error_matches, 1):
        print(f"  {i}. {error.strip()}")
else:
    # Try alternative error pattern
    error_matches = re.findall(r'<li[^>]*>([^<]*(?:required|invalid|error)[^<]*)</li>', response.text, re.IGNORECASE)
    if error_matches:
        print(f"\nForm Errors Found:")
        for i, error in enumerate(error_matches, 1):
            print(f"  {i}. {error.strip()}")

# Check if we're seeing form validation issues
if 'csrftoken' in session.cookies or 'csrftoken' in response.cookies:
    print("\nCSRF token present in cookies")

# Show available packages
print("\n\nChecking available packages in database...")
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elleden.settings')
django.setup()

from pages.models import CateringPackage, ConferenceBooking
packages = CateringPackage.objects.all()
print(f"Available catering packages: {list(packages.values('id', 'name'))}")

# Try to get form field choices
from pages.forms import ConferenceBookingForm
form = ConferenceBookingForm()
print(f"\nConference package choices: {form.fields['package'].queryset.values('id', 'name')[:5]}")
