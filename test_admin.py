#!/usr/bin/env python
"""
Test script to verify admin functionality
"""
import os
import sys
import django
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kapadiaschool.settings')
django.setup()

def test_admin_urls():
    """Test admin URLs accessibility"""
    
    # Setup requests session with retries
    session = requests.Session()
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    urls_to_test = [
        ('Direct Django (port 8000)', 'http://localhost:8000/admin/'),
        ('Through Nginx (port 80)', 'http://localhost/admin/'),
    ]
    
    print("Testing Admin Panel Accessibility:")
    print("=" * 60)
    
    for name, url in urls_to_test:
        try:
            response = session.get(url, timeout=10)
            if response.status_code == 200:
                # Check if it's actually the admin login page
                if 'Django administration' in response.text or 'admin/login' in response.text:
                    print(f"✓ {name}: WORKING (Status: {response.status_code})")
                    print(f"  URL: {url}")
                    print(f"  Content indicates Django admin login page")
                else:
                    print(f"? {name}: Response 200 but not admin page")
                    print(f"  URL: {url}")
            else:
                print(f"✗ {name}: HTTP {response.status_code}")
                print(f"  URL: {url}")
        except requests.exceptions.RequestException as e:
            print(f"✗ {name}: ERROR - {str(e)}")
            print(f"  URL: {url}")
        print()

def test_admin_models():
    """Test admin model registration"""
    from django.contrib import admin
    
    print("Checking Admin Model Registration:")
    print("=" * 60)
    
    expected_models = [
        'CarouselImage',
        'Celebration', 
        'CelebrationPhoto',
        'Gallery',
        'GalleryImage',
        'BranchPhoto',
        'User',
        'Group'
    ]
    
    registered_models = []
    for model, admin_instance in admin.site._registry.items():
        model_name = model.__name__
        registered_models.append(model_name)
        print(f"✓ {model_name}: Registered with {admin_instance.__class__.__name__}")
    
    print(f"\nTotal registered models: {len(registered_models)}")
    
    # Check if all expected models are registered
    missing_models = set(expected_models) - set(registered_models)
    if missing_models:
        print(f"⚠ Missing models: {', '.join(missing_models)}")
    else:
        print("✓ All expected models are registered!")

def test_users():
    """Test admin users"""
    from django.contrib.auth.models import User
    
    print("\nChecking Admin Users:")
    print("=" * 60)
    
    superusers = User.objects.filter(is_superuser=True, is_active=True)
    staff_users = User.objects.filter(is_staff=True, is_active=True)
    
    print(f"Active superusers: {superusers.count()}")
    for user in superusers:
        print(f"  - {user.username} ({user.email or 'no email'})")
    
    print(f"Active staff users: {staff_users.count()}")
    for user in staff_users:
        status = "SUPERUSER" if user.is_superuser else "STAFF"
        print(f"  - {user.username} ({user.email or 'no email'}) - {status}")

def main():
    print("Django Admin Panel Test")
    print("=" * 60)
    print()
    
    test_admin_urls()
    print()
    test_admin_models()
    print()
    test_users()
    
    print("\n" + "=" * 60)
    print("Admin Panel Test Complete!")
    print("\nTo access the admin panel:")
    print("- Direct: http://localhost:8000/admin/")
    print("- Via Nginx: http://localhost/admin/")
    print("\nExisting admin accounts:")
    print("- Username: admin")
    print("- Username: abc")
    print("(Use docker-compose exec web python manage.py manage_admin_users --reset-password <username> to reset passwords)")

if __name__ == "__main__":
    main()
