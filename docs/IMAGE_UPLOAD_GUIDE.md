# Image Upload Guide for Kapadia High School Website

## Recommended Image Dimensions

For optimal display on the website, please use the following image dimensions when uploading photos to different sections:

### 1. Carousel Images (Homepage Banner)
- **Dimensions:** 1920 x 600 pixels
- **Aspect Ratio:** 16:5 (widescreen landscape)
- **File Size:** Ideally under 500KB
- **Format:** JPG or PNG
- **Notes:** These images appear in the main homepage carousel. Use high-quality landscape photos with good contrast for text visibility.

### 2. Celebration Images
- **Dimensions:** 800 x 600 pixels
- **Aspect Ratio:** 4:3
- **File Size:** Ideally under 300KB
- **Format:** JPG or PNG
- **Notes:** These images are used for school events and celebrations.

### 3. Gallery Images (Full Size)
- **Dimensions:** 1200 x 800 pixels
- **Aspect Ratio:** 3:2
- **File Size:** Ideally under 400KB
- **Format:** JPG or PNG
- **Notes:** These are the main images displayed in the gallery modal when clicked.

### 4. Gallery Thumbnails
- **Dimensions:** 400 x 300 pixels
- **Aspect Ratio:** 4:3
- **File Size:** Ideally under 100KB
- **Format:** JPG or PNG
- **Notes:** These are the smaller preview images displayed in the gallery grid.

## Image Optimization Tips

1. **Crop your images** to the recommended aspect ratio before uploading
2. **Compress your images** using tools like TinyPNG, ImageOptim, or Photoshop's "Save for Web"
3. **Use descriptive filenames** as they help with SEO and organization
4. **Add alt text** when uploading to improve accessibility

## Supabase Storage Information

The website uses Supabase for image storage with the following buckets:
- `carousel-images`: For homepage carousel/banner images
- `celebration-images`: For celebration and event images
- `gallery-images`: For full-size gallery images
- `gallery-thumbnails`: For gallery preview thumbnails

## Image Management

### Uploading Images
Images are automatically uploaded to the appropriate Supabase bucket when you add them through the admin interface. The system will optimize and resize your images according to the recommended dimensions.

### Deleting Images
You can delete images through the admin interface. The system will automatically remove the files from the Supabase storage buckets.

### Important Notes
- The system automatically generates unique filenames to prevent conflicts
- Images are optimized before uploading to reduce bandwidth usage
- Public read access is enabled for all images to display them on the website
- Delete policies are configured to allow removing images when needed
