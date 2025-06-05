from django.contrib import admin
from khschool.models import Celebration, CarouselImage, CelebrationPhoto, Gallery, GalleryImage
from khschool.forms import CelebrationForm, CelebrationPhotoForm, CarouselImageForm, GalleryForm, GalleryImageForm

# Register your models here.

class CelebrationPhotoInline(admin.TabularInline):
    model = CelebrationPhoto
    form = CelebrationPhotoForm
    extra = 3  # Show 3 empty forms for adding photos
    fields = ('photo', 'photo_url', 'caption', 'order')
    readonly_fields = ('photo_url',)

@admin.register(CarouselImage)
class CarouselImageAdmin(admin.ModelAdmin):
    form = CarouselImageForm
    list_display = ('title', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'subtitle')
    readonly_fields = ('image_url',)

@admin.register(Celebration)
class CelebrationAdmin(admin.ModelAdmin):
    form = CelebrationForm
    list_display = ('festivalname', 'celebration_type', 'date', 'photo_count_display', 'preview_image')
    list_filter = ('date', 'celebration_type', 'is_featured')
    search_fields = ('festivalname', 'description')
    date_hierarchy = 'date'
    ordering = ('-date',)
    readonly_fields = ('image_url',)
    inlines = [CelebrationPhotoInline]
    
    def preview_image(self, obj):
        image_url = obj.get_image_url()
        if image_url:
            return f'<img src="{image_url}" width="50" height="50" style="object-fit: cover; border-radius: 5px;" />'
        return 'No Image'
    
    def photo_count_display(self, obj):
        count = obj.photo_count()
        return f'{count} photo{"s" if count != 1 else ""}'
    
    preview_image.allow_tags = True
    preview_image.short_description = 'Image Preview'
    photo_count_display.short_description = 'Additional Photos'

@admin.register(CelebrationPhoto)
class CelebrationPhotoAdmin(admin.ModelAdmin):
    form = CelebrationPhotoForm
    list_display = ('celebration', 'caption', 'order', 'preview_photo')
    list_filter = ('celebration',)
    list_editable = ('order',)
    readonly_fields = ('photo_url',)
    search_fields = ('celebration__festivalname', 'caption')
    
    def preview_photo(self, obj):
        photo_url = obj.get_photo_url()
        if photo_url:
            return f'<img src="{photo_url}" width="50" height="50" style="object-fit: cover; border-radius: 5px;" />'
        return 'No Image'
    
    preview_photo.allow_tags = True
    preview_photo.short_description = 'Photo Preview'


class GalleryImageInline(admin.TabularInline):
    model = GalleryImage
    form = GalleryImageForm
    extra = 3  # Show 3 empty forms for adding images
    fields = ('image', 'image_url', 'title', 'caption', 'order')
    readonly_fields = ('image_url',)


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    form = GalleryForm
    list_display = ('name', 'category', 'date_created', 'image_count_display', 'preview_thumbnail', 'is_featured')
    list_filter = ('category', 'date_created', 'is_featured')
    search_fields = ('name', 'description')
    date_hierarchy = 'date_created'
    ordering = ('-date_created',)
    readonly_fields = ('thumbnail_url',)
    inlines = [GalleryImageInline]
    
    def preview_thumbnail(self, obj):
        thumbnail_url = obj.get_thumbnail_url()
        if thumbnail_url:
            return f'<img src="{thumbnail_url}" width="50" height="50" style="object-fit: cover; border-radius: 5px;" />'
        return 'No Thumbnail'
    
    def image_count_display(self, obj):
        count = obj.image_count()
        return f'{count} image{"s" if count != 1 else ""}'
    
    preview_thumbnail.allow_tags = True
    preview_thumbnail.short_description = 'Thumbnail'
    image_count_display.short_description = 'Images'


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    form = GalleryImageForm
    list_display = ('gallery', 'title', 'order', 'date_added', 'preview_image')
    list_filter = ('gallery', 'date_added')
    list_editable = ('order',)
    readonly_fields = ('image_url',)
    search_fields = ('gallery__name', 'title', 'caption')
    date_hierarchy = 'date_added'
    
    def preview_image(self, obj):
        image_url = obj.get_image_url()
        if image_url:
            return f'<img src="{image_url}" width="50" height="50" style="object-fit: cover; border-radius: 5px;" />'
        return 'No Image'
    
    preview_image.allow_tags = True
    preview_image.short_description = 'Image Preview'