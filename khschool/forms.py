from django import forms
from .models import Celebration, CelebrationPhoto, CarouselImage, Gallery, GalleryImage
from .supabase_storage import upload_image, CAROUSEL_BUCKET, CELEBRATION_BUCKET, GALLERY_BUCKET, GALLERY_THUMBNAIL_BUCKET

class SupabaseImageUploadMixin:
    """Mixin to handle Supabase image uploads for model forms"""
    
    def save_image_to_supabase(self, image_field, bucket_name):
        """Upload image to Supabase and return the URL"""
        if image_field and hasattr(image_field, 'file'):
            # Upload the image to Supabase
            print(f"Uploading image to Supabase bucket: {bucket_name}")
            image_url = upload_image(image_field, bucket_name)
            print(f"Uploaded image URL: {image_url}")
            return image_url
        return None

class CelebrationForm(forms.ModelForm, SupabaseImageUploadMixin):
    """Form for Celebration model with Supabase image upload"""
    
    class Meta:
        model = Celebration
        fields = '__all__'
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Check if there's a new image to upload
        if 'image' in self.changed_data and self.cleaned_data.get('image'):
            image_url = self.save_image_to_supabase(
                self.cleaned_data['image'], 
                CELEBRATION_BUCKET
            )
            if image_url:
                instance.image_url = image_url
        
        if commit:
            instance.save()
        return instance

class CelebrationPhotoForm(forms.ModelForm, SupabaseImageUploadMixin):
    """Form for CelebrationPhoto model with Supabase image upload"""
    
    class Meta:
        model = CelebrationPhoto
        fields = '__all__'
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Check if there's a new photo to upload
        if 'photo' in self.changed_data and self.cleaned_data.get('photo'):
            photo_url = self.save_image_to_supabase(
                self.cleaned_data['photo'], 
                GALLERY_BUCKET
            )
            if photo_url:
                instance.photo_url = photo_url
        
        if commit:
            instance.save()
        return instance

class CarouselImageForm(forms.ModelForm, SupabaseImageUploadMixin):
    """Form for CarouselImage model with Supabase image upload"""
    
    class Meta:
        model = CarouselImage
        fields = '__all__'
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Check if there's a new image to upload
        if 'image' in self.changed_data and self.cleaned_data.get('image'):
            image_url = self.save_image_to_supabase(
                self.cleaned_data['image'], 
                CAROUSEL_BUCKET
            )
            if image_url:
                instance.image_url = image_url
        
        if commit:
            instance.save()
        return instance


class GalleryForm(forms.ModelForm, SupabaseImageUploadMixin):
    """Form for Gallery model with Supabase thumbnail upload"""
    
    class Meta:
        model = Gallery
        fields = '__all__'
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Check if there's a new thumbnail to upload
        if 'thumbnail' in self.changed_data and self.cleaned_data.get('thumbnail'):
            thumbnail_url = self.save_image_to_supabase(
                self.cleaned_data['thumbnail'], 
                GALLERY_THUMBNAIL_BUCKET
            )
            if thumbnail_url:
                instance.thumbnail_url = thumbnail_url
        
        if commit:
            instance.save()
        return instance


class GalleryImageForm(forms.ModelForm, SupabaseImageUploadMixin):
    """Form for GalleryImage model with Supabase image upload"""
    
    class Meta:
        model = GalleryImage
        fields = '__all__'
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Check if there's a new image to upload
        if 'image' in self.changed_data and self.cleaned_data.get('image'):
            image_url = self.save_image_to_supabase(
                self.cleaned_data['image'], 
                GALLERY_BUCKET
            )
            if image_url:
                instance.image_url = image_url
        
        if commit:
            instance.save()
        return instance
