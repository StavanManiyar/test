from django.db import models
from django.utils import timezone
from django.conf import settings
from django.db.models.signals import pre_delete
from django.dispatch import receiver
import os

# Create your models here.
class Celebration(models.Model):
    CELEBRATION_TYPES = [
        ('festival', 'Festival'),
        ('event', 'School Event'),
        ('sports', 'Sports Event'),
        ('cultural', 'Cultural Event'),
        ('academic', 'Academic Event'),
        ('other', 'Other'),
    ]
    
    festivalname = models.CharField(max_length=255, verbose_name='Celebration Name')
    description = models.TextField(blank=True, verbose_name='Description')
    celebration_type = models.CharField(max_length=20, choices=CELEBRATION_TYPES, default='festival', verbose_name='Type')
    # Original field for backward compatibility
    image = models.ImageField(upload_to='festival/images/', verbose_name='Main Image', blank=True, null=True)
    # Supabase image URL field
    image_url = models.CharField(max_length=500, verbose_name='Main Image (Supabase)', blank=True)
    date = models.DateTimeField(verbose_name='Date')
    is_featured = models.BooleanField(default=False, verbose_name='Feature on Homepage')
    
    class Meta:
        verbose_name = 'Celebration'
        verbose_name_plural = 'Celebrations'
        ordering = ['-date']
    
    def __str__(self):
        return self.festivalname
        
    def photo_count(self):
        """Return the number of additional photos for this celebration"""
        return self.celebrationphoto_set.count()

    def get_image_url(self):
        """Return the image URL for VPS deployment"""
        # For VPS deployment, prioritize local files
        if self.image:
            return self.image.url
        # Keep URL field as fallback for migration purposes
        if self.image_url:
            return self.image_url
        return None


class CelebrationPhoto(models.Model):
    """Model for additional photos for a celebration"""
    celebration = models.ForeignKey(Celebration, on_delete=models.CASCADE)
    # Original field for backward compatibility
    photo = models.ImageField(upload_to='festival/gallery/', verbose_name='Photo', blank=True, null=True)
    # Supabase image URL field
    photo_url = models.CharField(max_length=500, verbose_name='Photo (Supabase)', blank=True)
    caption = models.CharField(max_length=255, blank=True, verbose_name='Caption')
    order = models.IntegerField(default=0, verbose_name='Display Order')
    
    class Meta:
        verbose_name = 'Celebration Photo'
        verbose_name_plural = 'Celebration Photos'
        ordering = ['celebration', 'order']
        
    def __str__(self):
        return f"{self.celebration.festivalname} - Photo {self.order}"

    def get_photo_url(self):
        """Return the photo URL for VPS deployment"""
        # For VPS deployment, prioritize local files
        if self.photo:
            return self.photo.url
        # Keep URL field as fallback for migration purposes
        if self.photo_url:
            return self.photo_url
        return None

class Gallery(models.Model):
    """Model for gallery categories"""
    CATEGORY_CHOICES = [
        ('festival', 'Festival'),
        ('event', 'School Event'),
        ('sports', 'Sports Event'),
        ('cultural', 'Cultural Event'),
        ('academic', 'Academic Event'),
        ('other', 'Other'),
    ]
    
    # Campus branch choices
    CAMPUS_CHOICES = [
        ('chattral', 'Chattral Campus'),
        ('kadi', 'Kadi Campus'),
        ('iffco', 'IFFCO Campus'),
        ('chandkheda', 'Chandkheda Campus'),
        ('general', 'General/Other'),
    ]
    
    name = models.CharField(max_length=100, verbose_name='Gallery Name')
    description = models.TextField(blank=True, verbose_name='Description')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other', verbose_name='Category')
    # Campus branch field
    campus_branch = models.CharField(
        max_length=20, 
        choices=CAMPUS_CHOICES, 
        default='general', 
        verbose_name='Campus Branch'
    )
    # Show on campus page (for featured photos)
    show_on_campus_page = models.BooleanField(
        default=False, 
        verbose_name='Show on Campus Page (4-5 Featured Photos)'
    )
    # Thumbnail image
    thumbnail = models.ImageField(upload_to='gallery/thumbnails/', blank=True, null=True, verbose_name='Thumbnail')
    # Supabase thumbnail URL
    thumbnail_url = models.CharField(max_length=500, verbose_name='Thumbnail (Supabase)', blank=True)
    date_created = models.DateTimeField(default=timezone.now, verbose_name='Date Created')
    is_featured = models.BooleanField(default=False, verbose_name='Feature on Homepage')
    
    class Meta:
        verbose_name = 'Gallery'
        verbose_name_plural = 'Galleries'
        ordering = ['-date_created']
        indexes = [
            models.Index(fields=['campus_branch', 'show_on_campus_page']),
            models.Index(fields=['is_featured', '-date_created']),
            models.Index(fields=['category', '-date_created']),
            models.Index(fields=['campus_branch', 'category']),
        ]
    
    def __str__(self):
        return self.name
    
    def image_count(self):
        """Return the number of images in this gallery"""
        return self.galleryimage_set.count()
    
    def get_thumbnail_url(self):
        """Return the thumbnail URL for VPS deployment"""
        # For VPS deployment, prioritize local files
        if self.thumbnail:
            return self.thumbnail.url
        # Keep URL field as fallback for migration purposes
        if self.thumbnail_url:
            return self.thumbnail_url
        
        # If no thumbnail, try to get the first image in the gallery
        first_image = self.galleryimage_set.first()
        if first_image:
            return first_image.get_image_url()
        return None


class GalleryImage(models.Model):
    """Model for individual images in a gallery"""
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True, verbose_name='Title')
    # Original field for backward compatibility
    image = models.ImageField(upload_to='gallery/images/', blank=True, null=True, verbose_name='Image')
    # Supabase image URL field
    image_url = models.CharField(max_length=500, verbose_name='Image (Supabase)', blank=True)
    caption = models.CharField(max_length=255, blank=True, verbose_name='Caption')
    description = models.TextField(blank=True, verbose_name='Description')
    date_added = models.DateTimeField(default=timezone.now, verbose_name='Date Added')
    order = models.IntegerField(default=0, verbose_name='Display Order')
    
    class Meta:
        verbose_name = 'Gallery Image'
        verbose_name_plural = 'Gallery Images'
        ordering = ['gallery', 'order', '-date_added']
    
    def __str__(self):
        if self.title:
            return f"{self.gallery.name} - {self.title}"
        return f"{self.gallery.name} - Image {self.order}"
    
    def get_image_url(self):
        """Return the image URL for VPS deployment"""
        # For VPS deployment, prioritize local files
        if self.image:
            return self.image.url
        # Keep URL field as fallback for migration purposes
        if self.image_url:
            return self.image_url
        return None


class BranchPhoto(models.Model):
    """Model for direct campus/branch photo uploads"""
    CAMPUS_CHOICES = [
        ('chattral', 'Chattral Campus'),
        ('kadi', 'Kadi Campus'),
        ('iffco', 'IFFCO Campus'),
        ('chandkheda', 'Chandkheda Campus'),
    ]
    
    PHOTO_CATEGORY_CHOICES = [
        ('infrastructure', 'Infrastructure'),
        ('classrooms', 'Classrooms'),
        ('playground', 'Playground'),
        ('library', 'Library'),
        ('labs', 'Laboratories'),
        ('events', 'Events & Activities'),
        ('sports', 'Sports'),
        ('cultural', 'Cultural Activities'),
        ('facilities', 'Facilities'),
        ('campus_life', 'Campus Life'),
        ('other', 'Other'),
    ]
    
    campus_branch = models.CharField(
        max_length=20, 
        choices=CAMPUS_CHOICES,
        verbose_name='Campus Branch'
    )
    title = models.CharField(max_length=200, verbose_name='Photo Title')
    description = models.TextField(blank=True, verbose_name='Description')
    category = models.CharField(
        max_length=20, 
        choices=PHOTO_CATEGORY_CHOICES, 
        default='other',
        verbose_name='Photo Category'
    )
    
    # Dual storage support
    image = models.ImageField(
        upload_to='branch_photos/', 
        blank=True, 
        null=True, 
        verbose_name='Photo'
    )
    image_url = models.CharField(
        max_length=500, 
        verbose_name='Photo (Supabase)', 
        blank=True
    )
    
    is_featured = models.BooleanField(
        default=False, 
        verbose_name='Show on Campus Page'
    )
    order = models.IntegerField(default=0, verbose_name='Display Order')
    date_uploaded = models.DateTimeField(auto_now_add=True, verbose_name='Upload Date')
    
    class Meta:
        verbose_name = 'Branch Photo'
        verbose_name_plural = 'Branch Photos'
        ordering = ['campus_branch', 'order', '-date_uploaded']
        indexes = [
            models.Index(fields=['campus_branch', 'is_featured']),
            models.Index(fields=['campus_branch', 'category']),
        ]
    
    def __str__(self):
        return f"{self.get_campus_branch_display()} - {self.title}"
    
    def get_image_url(self):
        """Return the image URL, prioritizing local storage for VPS deployment"""
        # For VPS deployment, always use local storage first
        if self.image:
            return self.image.url
        # Fallback to Supabase URL if available (for migration purposes)
        if self.image_url:
            return self.image_url
        return None


class CarouselImage(models.Model):
    # URL choices for button links
    URL_CHOICES = [
        ('/', 'Home'),
        ('/aboutSchool/', 'About School'),
        ('/brief/', 'Executive Brief'),
        ('/gallery/', 'Gallery'),
        ('/contact/', 'Contact Us'),
        ('/chandkheda/', 'Chandkheda Campus'),
        ('/chattral/', 'Chattral Campus'),
        ('/iffco/', 'IFFCO Campus'),
        ('/kadi/', 'Kadi Campus'),
        ('#', 'No Link (Stay on Page)'),
    ]
    
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=200, blank=True)
    # Original field for backward compatibility
    image = models.ImageField(upload_to='carousel/images/', blank=True, null=True)
    # Supabase image URL field
    image_url = models.CharField(max_length=500, verbose_name='Image (Supabase)', blank=True)
    button_text = models.CharField(max_length=50, default='Learn More')
    button_link = models.CharField(max_length=100, choices=URL_CHOICES, default='/')
    order = models.IntegerField(default=0, help_text='Order in which to display the carousel image')
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
        verbose_name = 'Carousel Image'
        verbose_name_plural = 'Carousel Images'
    
    def __str__(self):
        return self.title

    def get_image_url(self):
        """Return the image URL for VPS deployment"""
        # For VPS deployment, prioritize local files
        if self.image:
            return self.image.url
        # Keep URL field as fallback for migration purposes
        if self.image_url:
            return self.image_url
        return None

# For VPS deployment, we use local file storage only
# The URL fields are kept for data migration purposes but not actively used

@receiver(pre_delete, sender=Celebration)
def delete_celebration_files(sender, instance, **kwargs):
    """Delete local image file when a Celebration is deleted"""
    if instance.image and os.path.isfile(instance.image.path):
        try:
            os.remove(instance.image.path)
            print(f"Deleted local image: {instance.image.path}")
        except Exception as e:
            print(f"Error deleting local image: {e}")

@receiver(pre_delete, sender=CelebrationPhoto)
def delete_celebration_photo_files(sender, instance, **kwargs):
    """Delete local photo file when a CelebrationPhoto is deleted"""
    if instance.photo and os.path.isfile(instance.photo.path):
        try:
            os.remove(instance.photo.path)
            print(f"Deleted local photo: {instance.photo.path}")
        except Exception as e:
            print(f"Error deleting local photo: {e}")

@receiver(pre_delete, sender=Gallery)
def delete_gallery_thumbnail_files(sender, instance, **kwargs):
    """Delete local thumbnail file when a Gallery is deleted"""
    if instance.thumbnail and os.path.isfile(instance.thumbnail.path):
        try:
            os.remove(instance.thumbnail.path)
            print(f"Deleted local thumbnail: {instance.thumbnail.path}")
        except Exception as e:
            print(f"Error deleting local thumbnail: {e}")

@receiver(pre_delete, sender=GalleryImage)
def delete_gallery_image_files(sender, instance, **kwargs):
    """Delete local image file when a GalleryImage is deleted"""
    if instance.image and os.path.isfile(instance.image.path):
        try:
            os.remove(instance.image.path)
            print(f"Deleted local gallery image: {instance.image.path}")
        except Exception as e:
            print(f"Error deleting local gallery image: {e}")

@receiver(pre_delete, sender=CarouselImage)
def delete_carousel_image_files(sender, instance, **kwargs):
    """Delete local image file when a CarouselImage is deleted"""
    if instance.image and os.path.isfile(instance.image.path):
        try:
            os.remove(instance.image.path)
            print(f"Deleted local carousel image: {instance.image.path}")
        except Exception as e:
            print(f"Error deleting local carousel image: {e}")

@receiver(pre_delete, sender=BranchPhoto)
def delete_branch_photo_files(sender, instance, **kwargs):
    """Delete local image file when a BranchPhoto is deleted"""
    if instance.image and os.path.isfile(instance.image.path):
        try:
            os.remove(instance.image.path)
            print(f"Deleted local branch photo: {instance.image.path}")
        except Exception as e:
            print(f"Error deleting local branch photo: {e}")
