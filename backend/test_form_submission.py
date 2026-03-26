import requests
from datetime import datetime, timedelta
import json
import re

# Test data
test_data = {
    'name': 'Test User',
    'email': 'test@example.com',
    'phone': '254712345678',
    'date': (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'),
    'meal_time': 'lunch',
    'time': '12:30',
    'guests': 4,
    'special_requests': 'No allergies'
}

# Make request
session = requests.Session()

# First, get the CSRF token
print("Fetching restaurant page...")
response = session.get('http://127.0.0.1:8000/restaurant/')

if response.status_code != 200:
    print(f"❌ Failed to fetch page: {response.status_code}")
    exit(1)

# Extract CSRF token from HTML
match = re.search(r"csrfmiddlewaretoken['\"]?\s*[:=]\s*['\"]([^'\"]+)", response.text)
csrf_token = match.group(1) if match else None

if not csrf_token:
    # Try alternative pattern
    match = re.search(r'<input[^>]*name=["\']csrfmiddlewaretoken["\'][^>]*value=["\']([^"\']+)["\']', response.text)
    csrf_token = match.group(1) if match else None

print(f"✓ CSRF Token found: {csrf_token[:20]}...\n")

# Add CSRF token to data
test_data['csrfmiddlewaretoken'] = csrf_token

# Submit the form  
print("Submitting restaurant form...")
response = session.post('http://127.0.0.1:8000/restaurant/', data=test_data, allow_redirects=False)
print(f"Status Code: {response.status_code}")

if response.status_code in [301, 302, 303, 307, 308]:
    redirect_url = response.headers.get('Location', 'N/A')
    print(f"✅ Redirect detected to: {redirect_url}")
    
    # Follow redirect
    full_url = f"http://127.0.0.1:8000{redirect_url}" if redirect_url.startswith('/') else redirect_url
    response = session.get(full_url)
    print(f"Following redirect, status: {response.status_code}")
    
    if 'confirmation' in redirect_url:
        print("✅ SUCCESS: Form submitted and redirected to confirmation page!")
    else:
        print("⚠️  Redirect received but not to confirmation page")
elif response.status_code == 200:
    if 'confirmation' in response.url:
        print("✅ SUCCESS: Form submitted and on confirmation page!")
    else:
        print("⚠️  Form submitted but not redirected to confirmation")
else:
    print(f"❌ Unexpected status: {response.status_code}")
    if response.text:
        print(f"Response preview: {response.text[:200]}")
