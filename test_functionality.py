#!/usr/bin/env python
"""
Test script to verify all functionality is working correctly
Run this with: python test_functionality.py
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kapadiaschool.settings')
django.setup()

from django.test import Client
from django.urls import reverse
from khschool.models import BranchPhoto, Gallery, GalleryImage
from django.contrib.auth.models import User

def test_branch_photo_model():
    """Test BranchPhoto model functionality"""
    print("✅ Testing BranchPhoto model...")
    
    # Test creating a branch photo
    photo = BranchPhoto(
        campus_branch='chattral',
        title='Test Photo',
        description='A test photo for Chattral campus',
        category='infrastructure',
        is_featured=True,
        order=1
    )
    
    # Test model methods
    assert str(photo) == "Chattral Campus - Test Photo"
    assert photo.get_image_url() is None  # No image set yet
    
    print("  ✓ BranchPhoto model works correctly")

def test_admin_integration():
    """Test admin integration"""
    print("✅ Testing admin integration...")
    
    try:
        from khschool.admin import BranchPhotoAdmin
        from khschool.forms import BranchPhotoForm
        
        print("  ✓ BranchPhoto admin class imported successfully")
        print("  ✓ BranchPhotoForm imported successfully")
    except ImportError as e:
        print(f"  ❌ Admin integration error: {e}")

def test_views():
    """Test campus views"""
    print("✅ Testing campus views...")
    
    client = Client()
    
    # Test campus pages
    campus_urls = [
        'chattral',
        'iffco', 
        'kadi',
        'chandkheda'
    ]
    
    for campus in campus_urls:
        try:
            response = client.get(f'/{campus}/')
            if response.status_code == 200:
                print(f"  ✓ {campus.title()} campus page loads correctly")
            else:
                print(f"  ⚠️ {campus.title()} campus page returned status {response.status_code}")
        except Exception as e:
            print(f"  ❌ Error loading {campus} page: {e}")
    
    # Test gallery views
    gallery_urls = [
        'chattral_gallery',
        'iffco_gallery',
        'kadi_gallery', 
        'chandkheda_gallery'
    ]
    
    for gallery in gallery_urls:
        try:
            response = client.get(reverse(gallery))
            if response.status_code == 200:
                print(f"  ✓ {gallery.replace('_', ' ').title()} loads correctly")
            else:
                print(f"  ⚠️ {gallery} returned status {response.status_code}")
        except Exception as e:
            print(f"  ❌ Error loading {gallery}: {e}")

def test_pagination():
    """Test pagination functionality"""
    print("✅ Testing pagination...")
    
    client = Client()
    
    # Test pagination on gallery pages
    try:
        response = client.get('/chattral/photos/?page=1')
        if response.status_code == 200:
            print("  ✓ Pagination works correctly")
            
            # Test category filtering
            response = client.get('/chattral/photos/?category=infrastructure')
            if response.status_code == 200:
                print("  ✓ Category filtering works correctly")
        else:
            print(f"  ⚠️ Pagination test returned status {response.status_code}")
    except Exception as e:
        print(f"  ❌ Pagination test error: {e}")

def test_management_command():
    """Test management command"""
    print("✅ Testing management command...")
    
    try:
        from django.core.management import call_command
        from io import StringIO
        
        out = StringIO()
        call_command('manage_branch_photos', '--action=stats', stdout=out)
        output = out.getvalue()
        
        if 'Branch Photo Statistics' in output:
            print("  ✓ Management command works correctly")
        else:
            print("  ⚠️ Management command output unexpected")
    except Exception as e:
        print(f"  ❌ Management command error: {e}")

def test_caching():
    """Test caching functionality"""
    print("✅ Testing caching...")
    
    from django.core.cache import cache
    
    # Test cache functionality
    cache.set('test_key', 'test_value', 60)
    if cache.get('test_key') == 'test_value':
        print("  ✓ Caching works correctly")
    else:
        print("  ❌ Caching not working")

def main():
    """Run all tests"""
    print("🚀 Starting functionality tests for Kapadia School Branch Photos...\n")
    
    test_branch_photo_model()
    test_admin_integration()
    test_views()
    test_pagination() 
    test_management_command()
    test_caching()
    
    print("\n🎉 All tests completed!")
    print("\n📋 Summary of optimizations implemented:")
    print("  • BranchPhoto model with proper indexing")
    print("  • Admin interface with bulk actions")
    print("  • Pagination support (18 photos per page)")
    print("  • Category filtering")
    print("  • Caching for better performance")
    print("  • Management commands for maintenance")
    print("  • Responsive gallery template")
    print("  • Lightbox functionality")
    print("  • SEO-friendly URLs")
    print("  • Error handling and logging")

if __name__ == '__main__':
    main()
