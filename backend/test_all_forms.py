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

def test_form(form_name, url, data, session):
    """Test form submission"""
    print(f"\n{'='*60}")
    print(f"Testing: {form_name}")
    print(f"{'='*60}")
    
    # Get CSRF token
    csrf_token = get_csrf_token(session, url)
    if not csrf_token:
        print(f"❌ Failed to get CSRF token")
        return False
    
    print(f"✓ CSRF Token found")
    
    # Add CSRF token
    data['csrfmiddlewaretoken'] = csrf_token
    
    # Submit form
    response = session.post(url, data=data, allow_redirects=False)
    
    if response.status_code in [301, 302, 303, 307, 308]:
        redirect_url = response.headers.get('Location', '')
        full_url = f"http://127.0.0.1:8000{redirect_url}" if redirect_url.startswith('/') else redirect_url
        
        # Follow redirect
        response = session.get(full_url)
        if response.status_code == 200 and 'confirmation' in redirect_url:
            print(f"✅ SUCCESS: Form submitted → redirected to {redirect_url}")
            return True
        else:
            print(f"⚠️  Form submitted but redirect issue")
            print(f"   Status: {response.status_code}, URL: {full_url}")
            return False
    else:
        print(f"❌ Failed: Status {response.status_code}")
        return False

# Session for cookies
session = requests.Session()

# Test 1: Restaurant Form
restaurant_data = {
    'name': 'John Doe',
    'email': 'john@example.com',
    'phone': '254712345678',
    'date': (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'),
    'meal_time': 'lunch',
    'time': '12:30',
    'guests': 4,
    'special_requests': ''
}

test_form(
    "Restaurant Reservation Form",
    "http://127.0.0.1:8000/restaurant/",
    restaurant_data.copy(),
    session
)

# Test 2: Conference Form
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
    'package': 'full_day',  # Use valid choice: half_day, full_day, residential, custom
    'seating_arrangement': 'theatre',  # Use valid choice: u_shape, classroom, banquet, theatre, boardroom
    'catering_required': False,
    'av_equipment_required': False,
    'additional_requirements': ''
}

test_form(
    "Conference Booking Form",
    "http://127.0.0.1:8000/conference/",
    conference_data.copy(),
    session
)

# Test 3: Catering Form (first check what packages exist)
catering_data = {
    'name': 'Alice Johnson',
    'email': 'alice@example.com',
    'phone': '254722222222',
    'event_date': (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d'),
    'event_time': '14:00',  # Add event time
    'event_type': 'wedding',
    'guest_count': 100,
    'venue_address': '123 Main Street, Nairobi',
    'package': 7,  # Use valid package ID (found from database)
    'special_requests': 'Vegetarian options needed'
}

test_form(
    "Catering Order Form",
    "http://127.0.0.1:8000/catering/",
    catering_data.copy(),
    session
)

print(f"\n{'='*60}")
print("✅ All form tests completed!")
print(f"{'='*60}")
