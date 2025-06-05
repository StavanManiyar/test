from django.db import models
from django.utils import timezone
from django.conf import settings
from django.db.models.signals import pre_delete
from django.dispatch import receiver

# Import the Supabase delete function
try:
    from .supabase_storage import delete_image
except ImportError:
    # Fallback if supabase_storage module is not available
    def delete_image(file_path, bucket_name):
        print(f"Mock delete: {file_path} from {bucket_name}")
        return False

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
        """Return the image URL, prioritizing Supabase URL in production"""
        # In production with Supabase configured, prioritize Supabase URLs
        if not settings.DEBUG and settings.USE_SUPABASE_STORAGE:
            if self.image_url:
                return self.image_url
            if self.image:
                return self.image.url
        # In development or without Supabase, prioritize local files
        else:
            if self.image:
                return self.image.url
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
        """Return the photo URL, prioritizing Supabase URL in production"""
        # In production with Supabase configured, prioritize Supabase URLs
        if not settings.DEBUG and settings.USE_SUPABASE_STORAGE:
            if self.photo_url:
                return self.photo_url
            if self.photo:
                return self.photo.url
        # In development or without Supabase, prioritize local files
        else:
            if self.photo:
                return self.photo.url
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
    
    name = models.CharField(max_length=100, verbose_name='Gallery Name')
    description = models.TextField(blank=True, verbose_name='Description')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other', verbose_name='Category')
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
    
    def __str__(self):
        return self.name
    
    def image_count(self):
        """Return the number of images in this gallery"""
        return self.galleryimage_set.count()
    
    def get_thumbnail_url(self):
        """Return the thumbnail URL, prioritizing Supabase URL in production"""
        # In production with Supabase configured, prioritize Supabase URLs
        if not settings.DEBUG and settings.USE_SUPABASE_STORAGE:
            if self.thumbnail_url:
                return self.thumbnail_url
            if self.thumbnail:
                return self.thumbnail.url
        # In development or without Supabase, prioritize local files
        else:
            if self.thumbnail:
                return self.thumbnail.url
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
        """Return the image URL, prioritizing Supabase URL in production"""
        # In production with Supabase configured, prioritize Supabase URLs
        if not settings.DEBUG and settings.USE_SUPABASE_STORAGE:
            if self.image_url:
                return self.image_url
            if self.image:
                return self.image.url
        # In development or without Supabase, prioritize local files
        else:
            if self.image:
                return self.image.url
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
        """Return the image URL, prioritizing Supabase URL in production"""
        # In production with Supabase configured, prioritize Supabase URLs
        if not settings.DEBUG and settings.USE_SUPABASE_STORAGE:
            if self.image_url:
                return self.image_url
            if self.image:
                return self.image.url
        # In development or without Supabase, prioritize local files
        else:
            if self.image:
                return self.image.url
            if self.image_url:
                return self.image_url
        
        return None

# Add signal receivers at the end of the file
@receiver(pre_delete, sender=Celebration)
def delete_celebration_image(sender, instance, **kwargs):
    """Delete the Supabase image when a Celebration is deleted"""
    if instance.image_url:
        # Extract file path from URL
        try:
            # URL format is typically https://...storage/v1/object/public/bucket-name/file-path
            parts = instance.image_url.split('/')
            bucket_index = parts.index('public') + 1
            bucket_name = parts[bucket_index]
            file_path = '/'.join(parts[bucket_index + 1:])
            
            # Delete from Supabase
            delete_image(file_path, bucket_name)
            print(f"Deleted image {file_path} from bucket {bucket_name}")
        except Exception as e:
            print(f"Error deleting Supabase image: {e}")

@receiver(pre_delete, sender=CelebrationPhoto)
def delete_celebration_photo(sender, instance, **kwargs):
    """Delete the Supabase photo when a CelebrationPhoto is deleted"""
    if instance.photo_url:
        try:
            parts = instance.photo_url.split('/')
            bucket_index = parts.index('public') + 1
            bucket_name = parts[bucket_index]
            file_path = '/'.join(parts[bucket_index + 1:])
            
            delete_image(file_path, bucket_name)
            print(f"Deleted photo {file_path} from bucket {bucket_name}")
        except Exception as e:
            print(f"Error deleting Supabase photo: {e}")

@receiver(pre_delete, sender=Gallery)
def delete_gallery_thumbnail(sender, instance, **kwargs):
    """Delete the Supabase thumbnail when a Gallery is deleted"""
    if instance.thumbnail_url:
        try:
            parts = instance.thumbnail_url.split('/')
            bucket_index = parts.index('public') + 1
            bucket_name = parts[bucket_index]
            file_path = '/'.join(parts[bucket_index + 1:])
            
            delete_image(file_path, bucket_name)
            print(f"Deleted thumbnail {file_path} from bucket {bucket_name}")
        except Exception as e:
            print(f"Error deleting Supabase thumbnail: {e}")

@receiver(pre_delete, sender=GalleryImage)
def delete_gallery_image(sender, instance, **kwargs):
    """Delete the Supabase image when a GalleryImage is deleted"""
    if instance.image_url:
        try:
            parts = instance.image_url.split('/')
            bucket_index = parts.index('public') + 1
            bucket_name = parts[bucket_index]
            file_path = '/'.join(parts[bucket_index + 1:])
            
            delete_image(file_path, bucket_name)
            print(f"Deleted gallery image {file_path} from bucket {bucket_name}")
        except Exception as e:
            print(f"Error deleting Supabase gallery image: {e}")

@receiver(pre_delete, sender=CarouselImage)
def delete_carousel_image(sender, instance, **kwargs):
    """Delete the Supabase image when a CarouselImage is deleted"""
    if instance.image_url:
        try:
            parts = instance.image_url.split('/')
            bucket_index = parts.index('public') + 1
            bucket_name = parts[bucket_index]
            file_path = '/'.join(parts[bucket_index + 1:])
            
            delete_image(file_path, bucket_name)
            print(f"Deleted carousel image {file_path} from bucket {bucket_name}")
        except Exception as e:
            print(f"Error deleting Supabase carousel image: {e}")