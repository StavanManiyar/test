#!/usr/bin/env python3
"""
Test script to verify campus gallery features are working correctly
"""

import os
import sys
import django
from django.test import TestCase, Client
from django.urls import reverse

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kapadiaschool.settings')
django.setup()

def test_campus_pages():
    """Test that all campus pages load correctly"""
    client = Client()
    
    campus_pages = [
        ('chattral', 'Chattral Campus'),
        ('kadi', 'Kadi Campus'),
        ('iffco', 'IFFCO Township Campus'),
        ('chandkheda', 'Chandkheda Campus')
    ]
    
    print("🏫 Testing Campus Pages...")
    print("-" * 50)
    
    for url_name, campus_name in campus_pages:
        try:
            response = client.get(f'/{url_name}/')
            if response.status_code == 200:
                print(f"✅ {campus_name}: Page loads successfully")
                
                # Check if campus gallery section is present
                content = response.content.decode('utf-8')
                if 'Campus Photo Gallery' in content:
                    print(f"   📸 Photo gallery section found")
                else:
                    print(f"   ❌ Photo gallery section missing")
                    
                if f'{url_name}_gallery' in content:
                    print(f"   🔗 Gallery link properly configured")
                else:
                    print(f"   ❌ Gallery link missing")
                    
            else:
                print(f"❌ {campus_name}: Failed to load (Status: {response.status_code})")
                
        except Exception as e:
            print(f"❌ {campus_name}: Error - {str(e)}")
        
        print()

def test_campus_gallery_pages():
    """Test that all campus gallery pages load correctly"""
    client = Client()
    
    gallery_pages = [
        ('chattral_gallery', 'Chattral Campus Gallery'),
        ('kadi_gallery', 'Kadi Campus Gallery'),
        ('iffco_gallery', 'IFFCO Campus Gallery'),
        ('chandkheda_gallery', 'Chandkheda Campus Gallery')
    ]
    
    print("🖼️ Testing Campus Gallery Pages...")
    print("-" * 50)
    
    for url_name, page_name in gallery_pages:
        try:
            response = client.get(f'/{url_name.replace("_gallery", "")}/photos/')
            if response.status_code == 200:
                print(f"✅ {page_name}: Gallery page loads successfully")
                
                # Check if gallery template is used
                content = response.content.decode('utf-8')
                if 'Photo Gallery' in content:
                    print(f"   📸 Gallery template loaded correctly")
                else:
                    print(f"   ❌ Gallery template issue")
                    
            else:
                print(f"❌ {page_name}: Failed to load (Status: {response.status_code})")
                
        except Exception as e:
            print(f"❌ {page_name}: Error - {str(e)}")
        
        print()

def test_database_models():
    """Test that database models are working correctly"""
    from khschool.models import Gallery, GalleryImage
    
    print("🗄️ Testing Database Models...")
    print("-" * 50)
    
    try:
        # Test Gallery model with campus branch
        gallery_count = Gallery.objects.count()
        print(f"✅ Gallery model working: {gallery_count} galleries found")
        
        # Test campus choices
        campus_choices = Gallery.CAMPUS_CHOICES
        print(f"✅ Campus choices available: {len(campus_choices)} campuses")
        for code, name in campus_choices:
            print(f"   - {name} ({code})")
        
        # Test GalleryImage model
        image_count = GalleryImage.objects.count()
        print(f"✅ GalleryImage model working: {image_count} images found")
        
        # Test campus filtering
        for code, name in campus_choices:
            campus_galleries = Gallery.objects.filter(campus_branch=code)
            featured_galleries = Gallery.objects.filter(
                campus_branch=code,
                show_on_campus_page=True
            )
            print(f"   {name}: {campus_galleries.count()} galleries, {featured_galleries.count()} featured")
            
    except Exception as e:
        print(f"❌ Database error: {str(e)}")
    
    print()

def test_admin_integration():
    """Test that admin interface includes campus features"""
    print("🔧 Testing Admin Integration...")
    print("-" * 50)
    
    try:
        from khschool.admin import GalleryAdmin
        from khschool.models import Gallery
        
        # Check if campus fields are in admin
        admin_instance = GalleryAdmin(Gallery, None)
        
        if 'campus_branch' in admin_instance.list_display:
            print("✅ Campus branch field in admin list")
        else:
            print("❌ Campus branch field missing from admin list")
            
        if 'show_on_campus_page' in admin_instance.list_display:
            print("✅ Featured flag field in admin list")
        else:
            print("❌ Featured flag field missing from admin list")
            
        if 'campus_branch' in admin_instance.list_filter:
            print("✅ Campus branch filter available")
        else:
            print("❌ Campus branch filter missing")
            
        if hasattr(admin_instance, 'actions'):
            actions = admin_instance.actions
            if any('campus_featured' in str(action) for action in actions):
                print("✅ Campus bulk actions available")
            else:
                print("❌ Campus bulk actions missing")
        
    except Exception as e:
        print(f"❌ Admin integration error: {str(e)}")
    
    print()

def main():
    """Run all tests"""
    print("🎯 CAMPUS GALLERY SYSTEM - TESTING ALL 4 BRANCHES")
    print("=" * 70)
    print()
    
    # Run all tests
    test_campus_pages()
    test_campus_gallery_pages()
    test_database_models()
    test_admin_integration()
    
    print("🎉 Testing completed!")
    print("\n📋 NEXT STEPS:")
    print("1. Start development server: python manage.py runserver")
    print("2. Visit campus pages:")
    print("   - http://127.0.0.1:8000/chattral/")
    print("   - http://127.0.0.1:8000/kadi/")
    print("   - http://127.0.0.1:8000/iffco/")
    print("   - http://127.0.0.1:8000/chandkheda/")
    print("3. Access admin panel: http://127.0.0.1:8000/admin")
    print("4. Add campus galleries and photos")
    print("5. Deploy to production using scripts/deploy.sh")

if __name__ == "__main__":
    main()
