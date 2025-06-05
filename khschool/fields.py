from django.db import models
from django.core.files.uploadedfile import UploadedFile
from .supabase_storage import upload_image, delete_image, CAROUSEL_BUCKET, CELEBRATION_BUCKET, GALLERY_BUCKET

class SupabaseImageField(models.CharField):
    """
    A custom field that stores images in Supabase storage and saves the URL in the database.
    """
    description = "An image field that stores images in Supabase"
    
    def __init__(self, bucket_name, folder="", *args, **kwargs):
        self.bucket_name = bucket_name
        self.folder = folder
        kwargs['max_length'] = 500  # URLs can be long
        super().__init__(*args, **kwargs)
    
    def pre_save(self, model_instance, add):
        """
        Handle the file upload to Supabase before saving the model
        """
        file = getattr(model_instance, self.attname)
        
        # If this is a file upload (UploadedFile), process it
        if isinstance(file, UploadedFile):
            # Upload the file to Supabase
            url = upload_image(file, self.bucket_name, self.folder)
            if url:
                # Set the URL as the field value
                setattr(model_instance, self.attname, url)
                return url
        
        # If it's already a string (URL) or upload failed, just return it
        return file
    
    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs['bucket_name'] = self.bucket_name
        kwargs['folder'] = self.folder
        del kwargs['max_length']  # We'll set this again in __init__
        return name, path, args, kwargs

# Convenience fields for different types of images
class CarouselImageField(SupabaseImageField):
    def __init__(self, *args, **kwargs):
        super().__init__(bucket_name=CAROUSEL_BUCKET, *args, **kwargs)

class CelebrationImageField(SupabaseImageField):
    def __init__(self, *args, **kwargs):
        super().__init__(bucket_name=CELEBRATION_BUCKET, *args, **kwargs)

class GalleryImageField(SupabaseImageField):
    def __init__(self, *args, **kwargs):
        super().__init__(bucket_name=GALLERY_BUCKET, *args, **kwargs)
