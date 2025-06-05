# Supabase Storage Integration for Kapadia High School

This document explains how to set up and use Supabase for cloud image storage in the Kapadia High School website.

## Why Supabase?

We've integrated Supabase storage to solve the 500 Internal Server Errors related to image handling in the deployed application. This approach:

1. Stores images in the cloud instead of the local filesystem
2. Avoids issues with static file serving on Render
3. Makes deployment more reliable
4. Allows for better scaling of media content

## Setup Instructions

### 1. Create a Supabase Account

1. Go to [Supabase](https://supabase.com/) and sign up for an account
2. Create a new project
3. Once your project is created, go to Project Settings > API
4. Copy the URL and anon/public key

### 2. Set Environment Variables

Add these environment variables to your local development environment and to your Render deployment:

```
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
```

For local development, you can add these to a `.env` file in the project root.

### 3. Initialize Supabase Storage

Run the initialization script to create the necessary storage buckets and apply migrations:

```
python initialize_supabase.py
```

This script will:
- Check your Supabase credentials
- Apply database migrations
- Create the required storage buckets (carousel, celebration, gallery)

## Using Supabase Storage in the Admin

The admin interface has been updated to work with both local files and Supabase storage:

1. **For new images**: Upload directly to Supabase
   - When adding a new image in the admin, it will be uploaded to Supabase and the URL stored in the database

2. **For existing images**: The system will continue to serve existing local images while also supporting new cloud-stored images

## Technical Details

### Storage Structure

We've created three separate buckets in Supabase:
- `carousel`: For homepage carousel images
- `celebration`: For main celebration images
- `gallery`: For additional celebration photos

### Model Changes

The models have been updated with new URL fields that store the Supabase image URLs:
- `image_url` for CarouselImage and Celebration models
- `photo_url` for CelebrationPhoto model

### Helper Methods

Each model now has a helper method to get the appropriate image URL:
- `get_image_url()` for CarouselImage and Celebration
- `get_photo_url()` for CelebrationPhoto

These methods prioritize the Supabase URL if available, falling back to the local file URL if needed.

## Troubleshooting

If you encounter issues with the Supabase integration:

1. **Check environment variables**: Make sure SUPABASE_URL and SUPABASE_KEY are correctly set
2. **Verify bucket creation**: Check if the required buckets exist in your Supabase project
3. **Check permissions**: Ensure the anon key has permissions to upload/read from the buckets
4. **Check migrations**: Run `python manage.py showmigrations` to verify all migrations are applied

## Reverting to Local Storage

If needed, you can continue using local storage by:
1. Uploading images using the original image fields in the admin
2. The system will automatically use these local images if no Supabase URL is available
