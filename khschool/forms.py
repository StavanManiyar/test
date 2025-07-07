from django import forms
from .models import Celebration, CelebrationPhoto, CarouselImage, Gallery, GalleryImage, BranchPhoto

# VPS-optimized forms using local storage only

class CelebrationForm(forms.ModelForm):
    """Form for Celebration model with local storage (VPS deployment)"""
    
    class Meta:
        model = Celebration
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'festivalname': forms.TextInput(attrs={'placeholder': 'Enter celebration name'}),
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class CelebrationPhotoForm(forms.ModelForm):
    """Form for CelebrationPhoto model with local storage (VPS deployment)"""
    
    class Meta:
        model = CelebrationPhoto
        fields = '__all__'
        widgets = {
            'caption': forms.TextInput(attrs={'placeholder': 'Enter photo caption'}),
        }

class CarouselImageForm(forms.ModelForm):
    """Form for CarouselImage model with local storage (VPS deployment)"""
    
    class Meta:
        model = CarouselImage
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter carousel title'}),
            'subtitle': forms.TextInput(attrs={'placeholder': 'Enter carousel subtitle'}),
            'button_text': forms.TextInput(attrs={'placeholder': 'Button text (e.g., Learn More)'}),
        }

class GalleryForm(forms.ModelForm):
    """Form for Gallery model with local storage (VPS deployment)"""
    
    class Meta:
        model = Gallery
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter gallery name'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class GalleryImageForm(forms.ModelForm):
    """Form for GalleryImage model with local storage (VPS deployment)"""
    
    class Meta:
        model = GalleryImage
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter image title'}),
            'caption': forms.TextInput(attrs={'placeholder': 'Enter image caption'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class BranchPhotoForm(forms.ModelForm):
    """Form for BranchPhoto model with local storage (VPS deployment)"""
    
    class Meta:
        model = BranchPhoto
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter photo title'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
