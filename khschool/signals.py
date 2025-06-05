from django.db.models.signals import pre_delete
from django.dispatch import receiver
import os
import re

from .models import CarouselImage, CelebrationPhoto, GalleryImage, Gallery, Celebration
from .supabase_storage import (
    delete_image, 
    CAROUSEL_BUCKET, 
    CELEBRATION_BUCKET, 
    GALLERY_BUCKET, 
    GALLERY_THUMBNAIL_BUCKET
)


def extract_filename_from_url(url):
    """
    Extract the filename from a Supabase URL
    Example: https://xytrskweguaviclqnrdx.supabase.co/storage/v1/object/public/carousel-images/image-123.jpg
    Returns: image-123.jpg
    """
    if not url:
        return None
    
    # Use regex to extract the filename from the URL
    match = re.search(r'/([^/]+)$', url)
    if match:
        return match.group(1)
    return None


@receiver(pre_delete, sender=CarouselImage)
def delete_carousel_image_from_supabase(sender, instance, **kwargs):
    """Delete carousel image from Supabase storage when the model instance is deleted"""
    if instance.image_url:
        print(f"Deleting carousel image from Supabase: {instance.image_url}")
        filename = extract_filename_from_url(instance.image_url)
        if filename:
            delete_image(filename, CAROUSEL_BUCKET)


@receiver(pre_delete, sender=Celebration)
def delete_celebration_image_from_supabase(sender, instance, **kwargs):
    """Delete celebration main image from Supabase storage when the model instance is deleted"""
    if instance.image_url:
        print(f"Deleting celebration image from Supabase: {instance.image_url}")
        filename = extract_filename_from_url(instance.image_url)
        if filename:
            delete_image(filename, CELEBRATION_BUCKET)


@receiver(pre_delete, sender=CelebrationPhoto)
def delete_celebration_photo_from_supabase(sender, instance, **kwargs):
    """Delete celebration photo from Supabase storage when the model instance is deleted"""
    if instance.photo_url:
        print(f"Deleting celebration photo from Supabase: {instance.photo_url}")
        filename = extract_filename_from_url(instance.photo_url)
        if filename:
            delete_image(filename, CELEBRATION_BUCKET)


@receiver(pre_delete, sender=Gallery)
def delete_gallery_thumbnail_from_supabase(sender, instance, **kwargs):
    """Delete gallery thumbnail from Supabase storage when the model instance is deleted"""
    if instance.thumbnail_url:
        print(f"Deleting gallery thumbnail from Supabase: {instance.thumbnail_url}")
        filename = extract_filename_from_url(instance.thumbnail_url)
        if filename:
            delete_image(filename, GALLERY_THUMBNAIL_BUCKET)


@receiver(pre_delete, sender=GalleryImage)
def delete_gallery_image_from_supabase(sender, instance, **kwargs):
    """Delete gallery image from Supabase storage when the model instance is deleted"""
    if instance.image_url:
        print(f"Deleting gallery image from Supabase: {instance.image_url}")
        filename = extract_filename_from_url(instance.image_url)
        if filename:
            delete_image(filename, GALLERY_BUCKET)
