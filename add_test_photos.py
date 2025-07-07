#!/usr/bin/env python
"""
Simple script to add test photos for development
Run this with: python add_test_photos.py
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kapadiaschool.settings')
django.setup()

from khschool.models import BranchPhoto
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile

def add_sample_photos():
    """Add sample photos for testing"""
    print("🎯 Adding sample photos for testing...")
    
    # Sample photo data
    sample_photos = [
        {
            'campus_branch': 'chattral',
            'title': 'Modern Classrooms',
            'description': 'State-of-the-art classrooms with smart boards',
            'category': 'classrooms',
            'is_featured': True,
            'order': 2
        },
        {
            'campus_branch': 'chattral',
            'title': 'Library Facility',
            'description': 'Well-equipped library with thousands of books',
            'category': 'library',
            'is_featured': True,
            'order': 3
        },
        {
            'campus_branch': 'iffco',
            'title': 'Sports Complex',
            'description': 'Modern sports facilities for all activities',
            'category': 'sports',
            'is_featured': True,
            'order': 2
        },
        {
            'campus_branch': 'kadi',
            'title': 'Science Laboratory',
            'description': 'Fully equipped science labs for experiments',
            'category': 'labs',
            'is_featured': True,
            'order': 2
        },
        {
            'campus_branch': 'chandkheda',
            'title': 'Campus Garden',
            'description': 'Beautiful green spaces for students',
            'category': 'facilities',
            'is_featured': True,
            'order': 2
        }
    ]
    
    # Check if we have existing image files
    image_files = []
    for root, dirs, files in os.walk('gallery/branch_photos/'):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                image_files.append(os.path.join('branch_photos', file))
    
    if not image_files:
        print("❌ No image files found in gallery/branch_photos/")
        print("Please add some image files to test with.")
        return
    
    created_count = 0
    for i, photo_data in enumerate(sample_photos):
        # Use existing image files cyclically
        image_path = image_files[i % len(image_files)]
        
        # Check if photo already exists
        existing = BranchPhoto.objects.filter(
            campus_branch=photo_data['campus_branch'],
            title=photo_data['title']
        ).first()
        
        if existing:
            print(f"  ⚠️ Photo '{photo_data['title']}' already exists for {photo_data['campus_branch']}")
            continue
        
        # Create the photo
        photo = BranchPhoto.objects.create(
            campus_branch=photo_data['campus_branch'],
            title=photo_data['title'],
            description=photo_data['description'],
            category=photo_data['category'],
            image=image_path,
            is_featured=photo_data['is_featured'],
            order=photo_data['order']
        )
        
        print(f"  ✅ Created: {photo.title} for {photo.get_campus_branch_display()}")
        created_count += 1
    
    print(f"\n🎉 Added {created_count} new photos!")
    
    # Show summary
    print("\n📊 Current Photo Summary:")
    for campus_code, campus_name in BranchPhoto.CAMPUS_CHOICES:
        count = BranchPhoto.objects.filter(campus_branch=campus_code).count()
        featured_count = BranchPhoto.objects.filter(
            campus_branch=campus_code, 
            is_featured=True
        ).count()
        print(f"  {campus_name}: {count} total, {featured_count} featured")

def clear_all_photos():
    """Clear all test photos (use with caution!)"""
    print("🗑️ Clearing all branch photos...")
    count = BranchPhoto.objects.count()
    BranchPhoto.objects.all().delete()
    print(f"Deleted {count} photos")

def main():
    """Main function"""
    if len(sys.argv) > 1 and sys.argv[1] == '--clear':
        clear_all_photos()
    else:
        add_sample_photos()

if __name__ == '__main__':
    main()
