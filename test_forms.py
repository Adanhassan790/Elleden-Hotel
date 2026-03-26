#!/usr/bin/env python
import urllib.request
import urllib.parse
import urllib.error
import sys

def test_form_submission(url, form_data):
    """Test form submission to a URL"""
    print(f"\n{'='*60}")
    print(f"Testing: {url}")
    print(f"{'='*60}")
    
    data = urllib.parse.urlencode(form_data).encode('utf-8')
    req = urllib.request.Request(url, data=data)
    req.add_header('User-Agent', 'Python Test Script')
    
    try:
        # Test without following redirects
        opener = urllib.request.build_opener(urllib.request.HTTPErrorProcessor)
        response = opener.open(req)
        print(f"✓ Status: {response.code}")
        print(f"✓ URL: {response.url}")
        print(f"✓ Content-Type: {response.headers.get('Content-Type')}")
        return True
    except urllib.error.HTTPError as e:
        print(f"✗ HTTP Error: {e.code}")
        print(f"✗ URL: {e.url}") 
        print(f"✗ Reason: {e.reason}")
        if e.code in [301, 302, 303, 307, 308]:
            print(f"✗ Redirect Location: {e.headers.get('Location')}")
        try:
            body = e.read().decode('utf-8', errors='ignore')[:300]
            if body:
                print(f"✗ Response Body: {body}")
        except:
            pass
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

# Test data for restaurant form
restaurant_data = {
    'name': 'Test User',
    'email': 'test@test.com',
    'phone': '1234567890',
    'date': '2026-04-10',
    'meal_time': 'Lunch',
    'time': '12:00',
    'guests': '5',
}

# Test data for conference form
conference_data = {
    'name': 'Test User',
    'email': 'test@test.com',
    'phone': '1234567890',
    'date': '2026-05-20',
    'participants': '50',
    'package': '1',
}

# Test data for catering form
catering_data = {
    'name': 'Test User',
    'email': 'test@test.com',
    'phone': '1234567890',
    'date': '2026-05-15',
    'persons': '100',
    'package': '1',
}

# Run tests
print("\n" + "="*60)
print("TESTING FORM SUBMISSIONS")
print("="*60)

test_form_submission('http://localhost:8000/restaurant/', restaurant_data)
test_form_submission('http://localhost:8000/conference/', conference_data)
test_form_submission('http://localhost:8000/catering/', catering_data)

print("\n" + "="*60)
