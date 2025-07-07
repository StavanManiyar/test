#!/usr/bin/env python
"""
Debug script for photo display issues
Run this with: python debug_photos.py
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kapadiaschool.settings')
django.setup()

from django.conf import settings
from khschool.models import BranchPhoto
from django.core.cache import cache

def check_media_configuration():
    """Check media files configuration"""
    print("🔧 Media Configuration:")
    print(f"  MEDIA_ROOT: {settings.MEDIA_ROOT}")
    print(f"  MEDIA_URL: {settings.MEDIA_URL}")
    print(f"  DEBUG mode: {settings.DEBUG}")
    print(f"  Media root exists: {os.path.exists(settings.MEDIA_ROOT)}")
    print()

def check_branch_photos():
    """Check BranchPhoto records in database"""
    print("📸 BranchPhoto Records:")
    photos = BranchPhoto.objects.all()
    print(f"  Total photos: {photos.count()}")
    
    if photos.exists():
        print("\n  Photo Details:")
        for photo in photos:
            print(f"    • {photo.title}")
            print(f"      Campus: {photo.get_campus_branch_display()}")
            print(f"      Category: {photo.get_category_display()}")
            print(f"      Featured: {'✅ Yes' if photo.is_featured else '❌ No'}")
            print(f"      Order: {photo.order}")
            print(f"      Image URL: {photo.get_image_url()}")
            
            # Check if file exists
            if photo.image:
                file_path = os.path.join(settings.MEDIA_ROOT, str(photo.image))
                file_exists = os.path.exists(file_path)
                print(f"      File exists: {'✅ Yes' if file_exists else '❌ No'}")
                if file_exists:
                    file_size = os.path.getsize(file_path)
                    print(f"      File size: {file_size:,} bytes")
            print()
    else:
        print("  ⚠️ No photos found in database")
    print()

def check_featured_photos_by_campus():
    """Check featured photos for each campus"""
    print("🏫 Featured Photos by Campus:")
    
    campuses = ['chattral', 'iffco', 'kadi', 'chandkheda']
    
    for campus in campuses:
        featured_photos = BranchPhoto.objects.filter(
            campus_branch=campus,
            is_featured=True
        ).order_by('order', '-date_uploaded')
        
        print(f"  {campus.title()} Campus: {featured_photos.count()} featured photos")
        for photo in featured_photos:
            print(f"    • {photo.title} (order: {photo.order})")
    print()

def check_media_url_accessibility():
    """Test if media URLs are properly configured for development"""
    print("🌐 Media URL Configuration:")
    
    from django.test import Client
    from django.urls import reverse
    
    client = Client()
    
    # Test a campus page
    try:
        response = client.get('/chattral/')
        print(f"  Chattral page status: {response.status_code}")
        
        # Check if the page contains image URLs
        if response.status_code == 200:
            content = response.content.decode()
            if '/gallery/' in content:
                print("  ✅ Media URLs found in page content")
            else:
                print("  ⚠️ No media URLs found in page content")
        
    except Exception as e:
        print(f"  ❌ Error accessing page: {e}")
    print()

def fix_common_issues():
    """Attempt to fix common photo display issues"""
    print("🔧 Attempting to fix common issues:")
    
    # 1. Mark photos as featured if none are featured
    total_photos = BranchPhoto.objects.count()
    featured_photos = BranchPhoto.objects.filter(is_featured=True).count()
    
    if total_photos > 0 and featured_photos == 0:
        print("  📌 No featured photos found. Marking recent photos as featured...")
        
        for campus in ['chattral', 'iffco', 'kadi', 'chandkheda']:
            recent_photos = BranchPhoto.objects.filter(
                campus_branch=campus
            ).order_by('-date_uploaded')[:3]
            
            for photo in recent_photos:
                photo.is_featured = True
                photo.save()
                print(f"    ✅ Marked '{photo.title}' as featured for {campus}")
    
    # 2. Clear cache
    cache.clear()
    print("  🗑️ Cleared Django cache")
    
    # 3. Check and create media directories
    media_dirs = [
        'branch_photos',
        'carousel',
        'festival',
        'thumbnails'
    ]
    
    for dir_name in media_dirs:
        dir_path = os.path.join(settings.MEDIA_ROOT, dir_name)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            print(f"  📁 Created directory: {dir_path}")
    
    print("  ✅ Fix attempts completed!")
    print()

def main():
    """Run all diagnostic checks"""
    print("🚀 Photo Display Diagnostic Tool\n")
    print("=" * 50)
    
    check_media_configuration()
    check_branch_photos()
    check_featured_photos_by_campus()
    check_media_url_accessibility()
    fix_common_issues()
    
    print("=" * 50)
    print("🎯 Quick Solutions:")
    print("1. If no photos show on campus pages:")
    print("   → Make sure photos are marked as 'featured' in admin")
    print("   → Check that photos exist in the gallery/ directory")
    print()
    print("2. If photos don't load (broken image icons):")
    print("   → Run development server with: python manage.py runserver")
    print("   → Check that MEDIA_URL is configured in main urls.py")
    print()
    print("3. To add photos via admin:")
    print("   → Go to http://127.0.0.1:8000/admin/")
    print("   → Branch Photos → Add Branch Photo")
    print("   → Upload image, select campus, mark as featured")
    print()
    print("4. To clear cache:")
    print("   → Run: python manage.py shell -c \"from django.core.cache import cache; cache.clear()\"")

if __name__ == '__main__':
    main()
