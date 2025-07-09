#!/usr/bin/env python
import os
import sys
import django
import requests

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kapadiaschool.settings')

# Setup Django
django.setup()

from django.urls import reverse
from django.test import Client

def test_urls():
    """Test all URLs to see which ones are working"""
    client = Client()
    
    urls_to_test = [
        ('home', '/'),
        ('gallery', '/gallery/'),
        ('contact', '/contact/'),
        ('brief', '/brief/'),
        ('aboutSchool', '/aboutSchool/'),
        ('chandkheda', '/chandkheda/'),
        ('chattral', '/chattral/'),
        ('iffco', '/iffco/'),
        ('kadi', '/kadi/'),
        ('admissions', '/admissions/'),
        ('facilities', '/facilities/'),
        ('activities', '/activities/'),
        ('celebrations', '/celebrations/'),
        ('testimonials', '/testimonials/'),
        ('our_team', '/our-team/'),
        ('success_stories', '/success-stories/'),
        ('achievements', '/achievements/'),
        ('blog', '/blog/'),
        ('campus_gallery', '/campus-gallery/'),
        ('carousel', '/carousel/'),
        ('gallery_new', '/gallery-new/'),
        ('institutional_goals', '/institutional-goals/'),
        ('team', '/team/'),
    ]
    
    print("Testing URLs:")
    print("-" * 60)
    
    for name, url in urls_to_test:
        try:
            response = client.get(url)
            status = "✓ OK" if response.status_code == 200 else f"✗ {response.status_code}"
            print(f"{name:20} {url:30} {status}")
        except Exception as e:
            print(f"{name:20} {url:30} ✗ ERROR: {str(e)}")

if __name__ == "__main__":
    test_urls()
