from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from .models import Celebration, CarouselImage, Gallery, GalleryImage, BranchPhoto
from django.core.paginator import Paginator
from django.db.models import Prefetch, Count, Q
from django.contrib import messages
import logging

# Setup logger
logger = logging.getLogger(__name__)
@cache_page(60 * 15)  # Cache for 15 minutes
def home(request):
    # Use cache key for expensive queries
    cache_key = 'homepage_data'
    cached_data = cache.get(cache_key)
    
    if cached_data:
        return render(request, 'home.html', cached_data)
    
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
            print(f"DEBUG: Found {len(carousel_images)} carousel images")
            for img in carousel_images:
                print(f"DEBUG: Carousel image - ID: {img.id}, Title: {img.title}, Image: {img.image}, URL: {img.get_image_url()}")
        except Exception as e:
            # Log the error but continue with empty list
            print(f"Error loading carousel images: {str(e)}")
    
    # Try to get featured galleries first with optimized query
    if 'khschool_gallery' in tables:
        try:
            featured_galleries = Gallery.objects.filter(
                is_featured=True
            ).prefetch_related(
                Prefetch(
                    'galleryimage_set',
                    queryset=GalleryImage.objects.order_by('order')[:4],
                    to_attr='sample_images'
                )
            ).order_by('-date_created')[:3]
        except Exception as e:
            # Log the error but continue with empty list
            print(f"Error loading featured galleries: {str(e)}")
    
    # If no featured galleries, fall back to celebrations
    if not featured_galleries and 'khschool_celebration' in tables:
        try:
            celebrations = Celebration.objects.select_related().order_by('-date')[:3]
        except Exception as e:
            # Log the error but continue with empty list
            print(f"Error loading celebrations: {str(e)}")
        
    context = {
        'carousel_images': carousel_images,
        'celebration': celebrations,
        'featured_galleries': featured_galleries
    }
    
    # Cache the context for 15 minutes
    cache.set(cache_key, context, 60 * 15)
    
    return render(request, 'home.html', context)

#gallery page
def gallery(request):
    # Get filter parameters
    category_filter = request.GET.get('category', None)
    branch_filter = request.GET.get('branch', None)
    
    # Check if the tables exist in the database
    from django.db import connection
    tables = connection.introspection.table_names()
    
    # Initialize variables
    galleries = []
    branch_photos = []
    celebrations = []
    
    # Get branch photos if branch filter is provided
    if branch_filter and 'khschool_branchphoto' in tables:
        try:
            # Get branch photos with optional category filter
            branch_photos_query = BranchPhoto.objects.filter(campus_branch=branch_filter)
            
            if category_filter and category_filter != 'all':
                branch_photos_query = branch_photos_query.filter(category=category_filter)
            
            branch_photos = branch_photos_query.order_by('order', '-date_uploaded')
            
        except Exception as e:
            print(f"Error loading branch photos: {str(e)}")
            branch_photos = []
    
    # Only try to query galleries if no branch filter or as additional content
    if not branch_filter and 'khschool_gallery' in tables:
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
    
    # For backward compatibility - also get celebrations if there are no galleries and no branch photos
    if not galleries and not branch_photos and 'khschool_celebration' in tables:
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
    
    # Add branch photo categories if branch photos exist
    if branch_photos:
        branch_categories = set(BranchPhoto.objects.values_list('category', flat=True).distinct())
        # Convert to display format
        branch_categories_display = [(cat, dict(BranchPhoto.PHOTO_CATEGORY_CHOICES).get(cat, cat.title())) for cat in branch_categories]
        categories = list(branch_categories)  # Use branch categories when viewing branch photos
    
    # Get available branches
    branches = [choice[0] for choice in BranchPhoto.CAMPUS_CHOICES] if 'khschool_branchphoto' in tables else []
    
    context = {
        'galleries': galleries,
        'branch_photos': branch_photos,
        'celebration': celebrations,  # Keep for backward compatibility
        'categories': categories,
        'branches': branches,
        'current_category': category_filter or 'all',
        'current_branch': branch_filter or 'all',
        'is_branch_view': bool(branch_filter),
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
@cache_page(60 * 10)  # Cache for 10 minutes
def chandkheda(request):
    # Use cache for featured photos
    cache_key = 'chandkheda_featured_photos'
    featured_photos = cache.get(cache_key)
    
    if featured_photos is None:
        # Get featured photos from BranchPhoto model
        featured_photos = BranchPhoto.objects.filter(
            campus_branch='chandkheda',
            is_featured=True
        ).order_by('order', '-date_uploaded')[:5]
        cache.set(cache_key, featured_photos, 60 * 10)  # Cache for 10 minutes
    
    context = {
        'campus_name': 'Chandkheda Campus',
        'featured_photos': featured_photos,
    }
    return render(request, 'chandkheda.html', context)

@cache_page(60 * 5)  # Cache for 5 minutes
def chandkheda_gallery_view(request):
    # Get all photos for Chandkheda campus using BranchPhoto model with pagination
    all_photos = BranchPhoto.objects.filter(
        campus_branch='chandkheda'
    ).order_by('order', '-date_uploaded')
    
    # Add pagination (18 photos per page for nice 3x6 grid)
    paginator = Paginator(all_photos, 18)
    page_number = request.GET.get('page')
    photos = paginator.get_page(page_number)
    
    # Get category filter if provided
    category_filter = request.GET.get('category')
    if category_filter and category_filter != 'all':
        all_photos = all_photos.filter(category=category_filter)
        paginator = Paginator(all_photos, 18)
        photos = paginator.get_page(page_number)
    
    # Get available categories for filtering
    available_categories = BranchPhoto.objects.filter(
        campus_branch='chandkheda'
    ).values_list('category', flat=True).distinct()
    
    context = {
        'campus_name': 'Chandkheda Campus',
        'photos': photos,
        'available_categories': available_categories,
        'current_category': category_filter or 'all',
        'total_photos': all_photos.count(),
    }
    return render(request, 'campus_gallery.html', context)

@cache_page(60 * 10)  # Cache for 10 minutes
def chattral(request):
    cache_key = 'chattral_featured_photos'
    featured_photos = cache.get(cache_key)
    
    if featured_photos is None:
        # Use BranchPhoto model for featured photos
        featured_photos = BranchPhoto.objects.filter(
            campus_branch='chattral',
            is_featured=True
        ).order_by('order', '-date_uploaded')[:5]
        cache.set(cache_key, featured_photos, 60 * 10)
    
    context = {
        'campus_name': 'Chattral Campus',
        'featured_photos': featured_photos,
    }
    return render(request, 'chattral.html', context)

@cache_page(60 * 5)  # Cache for 5 minutes
def chattral_gallery_view(request):
    # Get all photos for Chattral campus using BranchPhoto model with pagination
    all_photos = BranchPhoto.objects.filter(
        campus_branch='chattral'
    ).order_by('order', '-date_uploaded')
    
    # Add pagination
    paginator = Paginator(all_photos, 18)
    page_number = request.GET.get('page')
    photos = paginator.get_page(page_number)
    
    # Get category filter if provided
    category_filter = request.GET.get('category')
    if category_filter and category_filter != 'all':
        all_photos = all_photos.filter(category=category_filter)
        paginator = Paginator(all_photos, 18)
        photos = paginator.get_page(page_number)
    
    # Get available categories for filtering
    available_categories = BranchPhoto.objects.filter(
        campus_branch='chattral'
    ).values_list('category', flat=True).distinct()
    
    context = {
        'campus_name': 'Chattral Campus',
        'photos': photos,
        'available_categories': available_categories,
        'current_category': category_filter or 'all',
        'total_photos': all_photos.count(),
    }
    return render(request, 'campus_gallery.html', context)

@cache_page(60 * 10)  # Cache for 10 minutes
def iffco(request):
    cache_key = 'iffco_featured_photos'
    featured_photos = cache.get(cache_key)
    
    if featured_photos is None:
        # Use BranchPhoto model for featured photos
        featured_photos = BranchPhoto.objects.filter(
            campus_branch='iffco',
            is_featured=True
        ).order_by('order', '-date_uploaded')[:5]
        cache.set(cache_key, featured_photos, 60 * 10)
    
    context = {
        'campus_name': 'IFFCO Campus',
        'featured_photos': featured_photos,
    }
    return render(request, 'iffco.html', context)

@cache_page(60 * 5)  # Cache for 5 minutes
def iffco_gallery_view(request):
    # Get all photos for IFFCO campus using BranchPhoto model with pagination
    all_photos = BranchPhoto.objects.filter(
        campus_branch='iffco'
    ).order_by('order', '-date_uploaded')
    
    # Add pagination
    paginator = Paginator(all_photos, 18)
    page_number = request.GET.get('page')
    photos = paginator.get_page(page_number)
    
    # Get category filter if provided
    category_filter = request.GET.get('category')
    if category_filter and category_filter != 'all':
        all_photos = all_photos.filter(category=category_filter)
        paginator = Paginator(all_photos, 18)
        photos = paginator.get_page(page_number)
    
    # Get available categories for filtering
    available_categories = BranchPhoto.objects.filter(
        campus_branch='iffco'
    ).values_list('category', flat=True).distinct()
    
    context = {
        'campus_name': 'IFFCO Campus',
        'photos': photos,
        'available_categories': available_categories,
        'current_category': category_filter or 'all',
        'total_photos': all_photos.count(),
    }
    return render(request, 'campus_gallery.html', context)

@cache_page(60 * 10)  # Cache for 10 minutes
def kadi(request):
    cache_key = 'kadi_featured_photos'
    featured_photos = cache.get(cache_key)
    
    if featured_photos is None:
        # Use BranchPhoto model for featured photos
        featured_photos = BranchPhoto.objects.filter(
            campus_branch='kadi',
            is_featured=True
        ).order_by('order', '-date_uploaded')[:5]
        cache.set(cache_key, featured_photos, 60 * 10)
    
    context = {
        'campus_name': 'Kadi Campus',
        'featured_photos': featured_photos,
    }
    return render(request, 'kadi.html', context)

@cache_page(60 * 5)  # Cache for 5 minutes
def kadi_gallery_view(request):
    # Get all photos for Kadi campus using BranchPhoto model with pagination
    all_photos = BranchPhoto.objects.filter(
        campus_branch='kadi'
    ).order_by('order', '-date_uploaded')
    
    # Add pagination
    paginator = Paginator(all_photos, 18)
    page_number = request.GET.get('page')
    photos = paginator.get_page(page_number)
    
    # Get category filter if provided
    category_filter = request.GET.get('category')
    if category_filter and category_filter != 'all':
        all_photos = all_photos.filter(category=category_filter)
        paginator = Paginator(all_photos, 18)
        photos = paginator.get_page(page_number)
    
    # Get available categories for filtering
    available_categories = BranchPhoto.objects.filter(
        campus_branch='kadi'
    ).values_list('category', flat=True).distinct()
    
    context = {
        'campus_name': 'Kadi Campus',
        'photos': photos,
        'available_categories': available_categories,
        'current_category': category_filter or 'all',
        'total_photos': all_photos.count(),
    }
    return render(request, 'campus_gallery.html', context)

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

# Additional page views
def admissions(request):
    return render(request, 'admissions.html')

def facilities(request):
    return render(request, 'facilities.html')

def activities(request):
    return render(request, 'activities.html')

def celebrations(request):
    # Get celebrations from database if available
    celebrations = []
    try:
        celebrations = Celebration.objects.all().order_by('-date')
        for celebration in celebrations:
            celebration.additional_photos = celebration.celebrationphoto_set.all().order_by('order')
    except Exception as e:
        print(f"Error loading celebrations: {str(e)}")
    
    context = {
        'celebrations': celebrations
    }
    return render(request, 'celebrations.html', context)

def testimonials(request):
    return render(request, 'testimonials.html')

def our_team(request):
    return render(request, 'our_team.html')

def success_stories(request):
    return render(request, 'success_stories.html')

def achievements(request):
    return render(request, 'achievements.html')

def blog(request):
    return render(request, 'blog.html')

def campus_gallery(request):
    return render(request, 'campus_gallery.html')

def carousel(request):
    return render(request, 'carousel.html')

def gallery_new(request):
    return render(request, 'gallery_new.html')

def institutional_goals(request):
    return render(request, 'institutional_goals.html')

def team(request):
    return render(request, 'team.html')
