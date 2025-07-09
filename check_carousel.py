#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kapadiaschool.settings')

# Setup Django
django.setup()

from khschool.models import CarouselImage

def check_carousel_images():
    print("=== Carousel Images Check ===")
    print(f"Total carousel images: {CarouselImage.objects.count()}")
    print()
    
    for img in CarouselImage.objects.all():
        print(f"ID: {img.id}")
        print(f"Title: {img.title}")
        print(f"Image field: {img.image}")
        print(f"Image URL field: {img.image_url}")
        print(f"get_image_url(): {img.get_image_url()}")
        print(f"Is active: {img.is_active}")
        print(f"Order: {img.order}")
        print("-" * 50)

if __name__ == "__main__":
    check_carousel_images()
