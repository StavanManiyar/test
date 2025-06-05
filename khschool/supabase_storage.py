import os
import uuid
import requests
import io
from PIL import Image
from supabase import create_client, Client
from slugify import slugify
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile

# Initialize Supabase client
supabase_url = os.environ.get('SUPABASE_URL', '')
supabase_key = os.environ.get('SUPABASE_KEY', '')
supabase: Client = None

print(f"Supabase URL: {supabase_url[:10]}...")
print(f"Supabase Key: {supabase_key[:10]}...")

if supabase_url and supabase_key and supabase_url != 'your_supabase_url' and supabase_key != 'your_supabase_anon_key':
    try:
        supabase = create_client(supabase_url, supabase_key)
        print("Supabase client initialized successfully")
    except Exception as e:
        print(f"Error initializing Supabase client: {str(e)}")
else:
    print("WARNING: Supabase credentials not properly set or are using placeholder values")

# Bucket names for different types of media
CAROUSEL_BUCKET = "carousel-images"
CELEBRATION_BUCKET = "celebration-images"
GALLERY_BUCKET = "gallery-images"
GALLERY_THUMBNAIL_BUCKET = "gallery-thumbnails"

# Image dimensions for different sections
IMAGE_DIMENSIONS = {
    CAROUSEL_BUCKET: (1920, 600),  # Carousel images: landscape format for banners with fixed height
    CELEBRATION_BUCKET: (800, 600),  # Celebration images: standard format
    GALLERY_BUCKET: (1200, 800),  # Gallery images: landscape format for better viewing
    GALLERY_THUMBNAIL_BUCKET: (400, 300),  # Gallery thumbnails: smaller size for grid display
    'default': (1000, 1000)  # Default dimensions if bucket not specified
}

def initialize_supabase_client():
    """
    Initialize and return the Supabase client
    """
    global supabase
    if supabase:
        return supabase
        
    if supabase_url and supabase_key and supabase_url != 'your_supabase_url' and supabase_key != 'your_supabase_anon_key':
        try:
            supabase = create_client(supabase_url, supabase_key)
            print("Supabase client initialized successfully")
            return supabase
        except Exception as e:
            print(f"Error initializing Supabase client: {str(e)}")
            return None
    else:
        print("WARNING: Supabase credentials not properly set or are using placeholder values")
        return None

def check_buckets_exist():
    """
    Check if the required buckets exist in Supabase
    """
    if not supabase:
        print("WARNING: Supabase client not initialized. Cannot check buckets.")
        return False, []
    
    try:
        # Get list of existing buckets
        print("Checking for existing buckets...")
        buckets_response = supabase.storage.list_buckets()
        existing_buckets = [bucket['name'] for bucket in buckets_response]
        print(f"Found buckets: {existing_buckets}")
        
        # Check which required buckets exist
        required_buckets = [CAROUSEL_BUCKET, CELEBRATION_BUCKET, GALLERY_BUCKET, GALLERY_THUMBNAIL_BUCKET]
        missing_buckets = [bucket for bucket in required_buckets if bucket not in existing_buckets]
        
        if missing_buckets:
            print("The following buckets are missing and need to be created:")
            for bucket in missing_buckets:
                print(f"  - {bucket}")
            return False, missing_buckets
        else:
            print("All required buckets exist!")
            return True, []
    except Exception as e:
        print(f"Error checking buckets: {str(e)}")
        import traceback
        traceback.print_exc()
        return False, [CAROUSEL_BUCKET, CELEBRATION_BUCKET, GALLERY_BUCKET, GALLERY_THUMBNAIL_BUCKET]

def initialize_buckets():
    """
    Initialize Supabase storage buckets if they don't exist
    """
    if not supabase:
        print("WARNING: Supabase client not initialized. Cannot create buckets.")
        print("Please create the following buckets manually in your Supabase dashboard:")
        print(f"  - {CAROUSEL_BUCKET}")
        print(f"  - {CELEBRATION_BUCKET}")
        print(f"  - {GALLERY_BUCKET}")
        print(f"  - {GALLERY_THUMBNAIL_BUCKET}")
        print("\nAnd set the following bucket policies:")
        print("  - Allow public access for viewing images")
        print("  - For upload/delete, you may want to restrict to authenticated users only")
        return False
    
    # First check if buckets exist
    buckets_exist, missing_buckets = check_buckets_exist()
    if buckets_exist:
        return True
    
    try:
        # Create missing buckets
        print("\nAttempting to create missing buckets...")
        for bucket_name in missing_buckets:
            try:
                print(f"Creating bucket: {bucket_name}")
                supabase.storage.create_bucket(bucket_name, {'public': True})
                print(f"Successfully created bucket: {bucket_name}")
            except Exception as e:
                print(f"Error creating bucket {bucket_name}: {str(e)}")
                print("Please create this bucket manually in your Supabase dashboard")
        
        # Check again if all buckets now exist
        buckets_exist, still_missing = check_buckets_exist()
        if still_missing:
            print("\nSome buckets could not be created automatically.")
            print("Please create the following buckets manually in your Supabase dashboard:")
            for bucket in still_missing:
                print(f"  - {bucket}")
            print("\nAnd set the following bucket policies:")
            print("  - Allow public access for viewing images")
            print("  - For upload/delete, you may want to restrict to authenticated users only")
        
        return buckets_exist
    except Exception as e:
        print(f"Error initializing buckets: {str(e)}")
        return False

def optimize_image(image_file, bucket_name):
    """
    Optimize an image for web display by resizing and compressing
    
    Args:
        image_file: The image file object (from request.FILES)
        bucket_name: The bucket name to determine optimal dimensions
        
    Returns:
        An optimized image file object or the original if optimization fails
    """
    try:
        # Get target dimensions based on bucket
        target_width, target_height = IMAGE_DIMENSIONS.get(bucket_name, IMAGE_DIMENSIONS['default'])
        
        # Open the image using PIL
        image = Image.open(image_file)
        
        # Get original format
        format_name = image.format if image.format else 'JPEG'
        content_type = f'image/{format_name.lower()}'
        if format_name.lower() == 'jpg':
            content_type = 'image/jpeg'
            format_name = 'JPEG'
        
        # Calculate new dimensions while preserving aspect ratio
        original_width, original_height = image.size
        ratio = min(target_width/original_width, target_height/original_height)
        new_width = int(original_width * ratio)
        new_height = int(original_height * ratio)
        
        # Only resize if the image is larger than target dimensions
        if original_width > target_width or original_height > target_height:
            print(f"Resizing image from {original_width}x{original_height} to {new_width}x{new_height}")
            image = image.resize((new_width, new_height), Image.LANCZOS)
        
        # Save the optimized image to a BytesIO object
        output = io.BytesIO()
        
        # Determine quality based on format
        quality = 85  # Default quality for JPEG
        if format_name == 'JPEG':
            image.save(output, format=format_name, quality=quality, optimize=True)
        elif format_name == 'PNG':
            image.save(output, format=format_name, optimize=True)
        else:
            image.save(output, format=format_name)
        
        # Reset file pointer
        output.seek(0)
        
        # Create a new InMemoryUploadedFile from the optimized image
        optimized_file = InMemoryUploadedFile(
            file=output,
            field_name=image_file.field_name,
            name=image_file.name,
            content_type=content_type,
            size=output.tell(),
            charset=None
        )
        
        # Reset the file pointer for reading
        optimized_file.seek(0)
        
        print(f"Image optimized: {image_file.name} - New size: {optimized_file.size} bytes")
        return optimized_file
    
    except Exception as e:
        print(f"Error optimizing image: {str(e)}")
        # Reset the original file pointer and return it
        image_file.seek(0)
        return image_file

def upload_image(image_file, bucket_name, folder=""):
    """
    Upload an image to Supabase storage
    
    Args:
        image_file: The image file object (from request.FILES)
        bucket_name: The name of the bucket to upload to
        folder: Optional subfolder within the bucket
    
    Returns:
        The public URL of the uploaded image or None if upload failed
    """
    if not supabase:
        print("ERROR: Supabase client not initialized. Cannot upload image.")
        return None
    
    try:
        print(f"Starting upload process for file: {image_file.name} to bucket: {bucket_name}")
        
        # Optimize the image before uploading
        optimized_image = optimize_image(image_file, bucket_name)
        
        # Generate a unique filename to avoid collisions
        original_name = image_file.name
        file_extension = os.path.splitext(original_name)[1].lower()
        
        # Create a slug from the original filename and append a UUID
        name_slug = slugify(os.path.splitext(original_name)[0])
        unique_filename = f"{name_slug}-{uuid.uuid4().hex[:8]}{file_extension}"
        
        # Construct the path in the bucket
        path = unique_filename
        if folder:
            path = f"{folder}/{unique_filename}"
        
        print(f"Uploading file to path: {path}")
        
        # Read the file content
        file_content = optimized_image.read()
        print(f"File size after optimization: {len(file_content)} bytes")
        
        # Upload the file
        print("Attempting to upload to Supabase...")
        upload_result = supabase.storage.from_(bucket_name).upload(
            path, 
            file_content,
            {"content-type": optimized_image.content_type if hasattr(optimized_image, 'content_type') else 'image/jpeg'}
        )
        print(f"Upload result: {upload_result}")
        
        # Get the public URL
        public_url = supabase.storage.from_(bucket_name).get_public_url(path)
        print(f"Generated public URL: {public_url}")
        return public_url
    
    except Exception as e:
        print(f"ERROR uploading to Supabase: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def delete_image(file_path, bucket_name):
    """
    Delete an image from Supabase storage
    
    Args:
        file_path: The path of the file in the bucket
        bucket_name: The name of the bucket
    
    Returns:
        True if deletion was successful, False otherwise
    """
    if not supabase:
        return False
    
    try:
        supabase.storage.from_(bucket_name).remove([file_path])
        return True
    except Exception as e:
        print(f"Error deleting from Supabase: {str(e)}")
        return False

def get_image_from_url(url):
    """
    Fetch an image from a URL and return it as a file-like object
    Useful for migrating existing images to Supabase
    
    Args:
        url: The URL of the image to fetch
    
    Returns:
        A tuple of (file-like object, filename) or (None, None) if fetch failed
    """
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            # Get the filename from the URL
            filename = os.path.basename(url)
            return response.raw, filename
        return None, None
    except Exception as e:
        print(f"Error fetching image from URL: {str(e)}")
        return None, None
