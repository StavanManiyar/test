from django.shortcuts import render
from django.http import HttpResponse
from .models import Celebration, CarouselImage, CelebrationPhoto, Gallery, GalleryImage
from django.contrib.auth.decorators import login_required
# Create your views here.
def home(request):
    # Set default empty values
    carousel_images = []
    celebrations = []
    featured_galleries = []
    
    # Check if the tables exist in the database
    from django.db import connection
    tables = connection.introspection.table_names()
    
    # Only try to query if the tables exist
    if 'khschool_carouselimage' in tables:
        try:
            carousel_images = CarouselImage.objects.filter(is_active=True).order_by('order')
        except Exception as e:
            # Log the error but continue with empty list
            print(f"Error loading carousel images: {str(e)}")
    
    # Try to get featured galleries first
    if 'khschool_gallery' in tables:
        try:
            featured_galleries = Gallery.objects.filter(is_featured=True).order_by('-date_created')[:3]
            # For each gallery, get a sample of images
            for gallery in featured_galleries:
                gallery.sample_images = gallery.galleryimage_set.all().order_by('order')[:4]
        except Exception as e:
            # Log the error but continue with empty list
            print(f"Error loading featured galleries: {str(e)}")
    
    # If no featured galleries, fall back to celebrations
    if not featured_galleries and 'khschool_celebration' in tables:
        try:
            celebrations = Celebration.objects.all().order_by('-date')[:3]
        except Exception as e:
            # Log the error but continue with empty list
            print(f"Error loading celebrations: {str(e)}")
        
    context = {
        'carousel_images': carousel_images,
        'celebration': celebrations,
        'featured_galleries': featured_galleries
    }
    
    return render(request, 'home.html', context)

#gallery page
def gallery(request):
    # Set default empty values
    galleries = []
    category_filter = request.GET.get('category', None)
    
    # Check if the tables exist in the database
    from django.db import connection
    tables = connection.introspection.table_names()
    
    # Only try to query if the Gallery table exists
    if 'khschool_gallery' in tables:
        try:
            # Get galleries with optional category filter
            if category_filter and category_filter != 'all':
                galleries = Gallery.objects.filter(category=category_filter).order_by('-date_created')
            else:
                galleries = Gallery.objects.all().order_by('-date_created')
            
            # For each gallery, get its images
            for gallery in galleries:
                try:
                    images = gallery.galleryimage_set.all().order_by('order', '-date_added')
                    gallery.images = list(images)
                    gallery.image_count = len(gallery.images)
                except Exception as e:
                    print(f"Error loading images for gallery {gallery.id}: {str(e)}")
                    gallery.images = []
                    gallery.image_count = 0
        except Exception as e:
            print(f"Error loading galleries: {str(e)}")
            galleries = []
    
    # For backward compatibility - also get celebrations if there are no galleries
    celebrations = []
    if not galleries and 'khschool_celebration' in tables:
        try:
            celebrations = Celebration.objects.all().order_by('-date')
            for celebration in celebrations:
                try:
                    photos = celebration.celebrationphoto_set.all().order_by('order')
                    celebration.additional_photos = list(photos)
                    celebration.photo_count = len(celebration.additional_photos)
                except Exception as e:
                    print(f"Error loading additional photos for celebration {celebration.id}: {str(e)}")
                    celebration.additional_photos = []
                    celebration.photo_count = 0
        except Exception as e:
            print(f"Error loading celebrations: {str(e)}")
            celebrations = []
    
    # Get all available categories for the filter
    categories = [choice[0] for choice in Gallery.CATEGORY_CHOICES]
    
    context = {
        'galleries': galleries,
        'celebration': celebrations,  # Keep for backward compatibility
        'categories': categories,
        'current_category': category_filter or 'all'
    }
    
    return render(request, 'gallery.html', context)

#contact page
def contact(request):
    return render(request,'contact.html')

#Director-brief
def brief(request):
    return render(request,'brief.html')

#school-history
def aboutSchool(request):
    return render(request,'aboutSchool.html')

#memnagar campus page
def chandkheda(request):
    return render(request,'chandkheda.html')

def chattral(request):
    return render(request,'chattral.html')

def iffco(request):
    return render(request,'iffco.html')

def kadi(request):
    return render(request,'kadi.html')

#success stories page
def success_stories(request):
    return render(request,'success_stories.html')

#facilities page
def facilities(request):
    return render(request,'facilities.html')

#admissions page
def admissions(request):
    return render(request,'admissions.html')

#institutional goals page
def institutional_goals(request):
    return render(request,'institutional_goals.html')

#our team page
def our_team(request):
    return render(request,'our_team.html')

#team page
def team(request):
    return render(request,'team.html')

#activities page
def activities(request):
    return render(request,'activities.html')

#testimonials page
def testimonials(request):
    return render(request,'testimonials.html')

#blog page
def blog(request):
    return render(request,'blog.html')

#achievements page
def achievements(request):
    return render(request,'achievements.html')

@login_required
def image_test(request):
    """
    View for testing image display from Supabase storage
    Protected by login to prevent public access
    """
    carousel_images = CarouselImage.objects.filter(is_active=True).order_by('order')
    celebrations = Celebration.objects.all().order_by('-date')
    galleries = Gallery.objects.all().order_by('-date_created')
    
    # For each celebration, get its additional photos
    for celebration in celebrations:
        celebration.additional_photos = celebration.celebrationphoto_set.all().order_by('order')
    
    # For each gallery, get its images
    for gallery in galleries:
        gallery.images = gallery.galleryimage_set.all().order_by('order', '-date_added')
    
    context = {
        'carousel_images': carousel_images,
        'celebrations': celebrations,
        'galleries': galleries
    }
    
    return render(request, 'image_test.html', context)
