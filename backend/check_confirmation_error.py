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

# Test conference form submission
print("Testing Conference Form Submission...")
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
    'package': 'full_day',
    'seating_arrangement': 'theatre',
    'catering_required': False,
    'av_equipment_required': False,
    'csrfmiddlewaretoken': csrf_token
}

response = session.post("http://127.0.0.1:8000/conference/", data=conference_data, allow_redirects=False)

if response.status_code in [301, 302, 303, 307, 308]:
    redirect_url = response.headers.get('Location', '')
    full_url = f"http://127.0.0.1:8000{redirect_url}" if redirect_url.startswith('/') else redirect_url
    print(f"✓ Redirected to: {redirect_url}\n")
    
    # Follow redirect
    response = session.get(full_url)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 500:
        print("❌ 500 Error on confirmation page!")
        # Try to extract error info
        if '<h1>' in response.text:
            match = re.search(r'<h1[^>]*>([^<]+)</h1>', response.text)
            if match:
                print(f"Error heading: {match.group(1)}")
        if 'TemplateDoesNotExist' in response.text:
            print("Error type: Template not found")
        if 'Traceback' in response.text:
            # Extract traceback
            lines = response.text.split('<br>')[:10]
            for line in lines:
                line = re.sub(r'<[^>]+>', '', line)
                if line.strip():
                    print(f"  {line[:100]}")

