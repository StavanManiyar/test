from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, GroupAdmin as BaseGroupAdmin
from django.core.exceptions import PermissionDenied
from django.contrib.admin.views.main import ChangeList
from django.contrib import messages
from django.http import HttpResponseForbidden
from khschool.models import Celebration, CarouselImage, CelebrationPhoto, Gallery, GalleryImage, BranchPhoto
from khschool.forms import CelebrationForm, CelebrationPhotoForm, CarouselImageForm, GalleryForm, GalleryImageForm, BranchPhotoForm

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
    list_display = ('name', 'campus_branch', 'category', 'show_on_campus_page', 'date_created', 'image_count_display', 'preview_thumbnail', 'is_featured')
    list_filter = ('campus_branch', 'category', 'show_on_campus_page', 'date_created', 'is_featured')
    search_fields = ('name', 'description')
    date_hierarchy = 'date_created'
    ordering = ('-date_created',)
    readonly_fields = ('thumbnail_url',)
    inlines = [GalleryImageInline]
    
    # Add bulk actions for campus management
    actions = ['mark_as_campus_featured', 'unmark_as_campus_featured']
    
    def mark_as_campus_featured(self, request, queryset):
        queryset.update(show_on_campus_page=True)
        self.message_user(request, f'{queryset.count()} galleries marked as campus featured.')
    mark_as_campus_featured.short_description = 'Mark selected galleries as campus featured'
    
    def unmark_as_campus_featured(self, request, queryset):
        queryset.update(show_on_campus_page=False)
        self.message_user(request, f'{queryset.count()} galleries unmarked as campus featured.')
    unmark_as_campus_featured.short_description = 'Unmark selected galleries as campus featured'
    
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


@admin.register(BranchPhoto)
class BranchPhotoAdmin(admin.ModelAdmin):
    form = BranchPhotoForm
    list_display = ('title', 'campus_branch', 'category', 'is_featured', 'order', 'date_uploaded', 'preview_image')
    list_filter = ('campus_branch', 'category', 'is_featured', 'date_uploaded')
    list_editable = ('is_featured', 'order')
    search_fields = ('title', 'description')
    readonly_fields = ('image_url', 'date_uploaded')
    date_hierarchy = 'date_uploaded'
    ordering = ('campus_branch', 'order', '-date_uploaded')
    
    # Add bulk actions for campus management
    actions = ['mark_as_featured', 'unmark_as_featured']
    
    def mark_as_featured(self, request, queryset):
        queryset.update(is_featured=True)
        self.message_user(request, f'{queryset.count()} photos marked as featured.')
    mark_as_featured.short_description = 'Mark selected photos as featured'
    
    def unmark_as_featured(self, request, queryset):
        queryset.update(is_featured=False)
        self.message_user(request, f'{queryset.count()} photos unmarked as featured.')
    unmark_as_featured.short_description = 'Unmark selected photos as featured'
    
    def preview_image(self, obj):
        image_url = obj.get_image_url()
        if image_url:
            return f'<img src="{image_url}" width="50" height="50" style="object-fit: cover; border-radius: 5px;" />'
        return 'No Image'
    
    preview_image.allow_tags = True
    preview_image.short_description = 'Photo Preview'
    
    # Organize by campus in admin
    fieldsets = (
        ('Campus Information', {
            'fields': ('campus_branch', 'title', 'description')
        }),
        ('Photo Details', {
            'fields': ('category', 'image', 'image_url')
        }),
        ('Display Settings', {
            'fields': ('is_featured', 'order')
        }),
        ('Date Information', {
            'fields': ('date_uploaded',),
            'classes': ('collapse',)
        })
    )

# Security Enhancement: Custom User Admin with restrictions
class SecureUserAdmin(BaseUserAdmin):
    """Custom User Admin with security restrictions"""
    
    def get_queryset(self, request):
        # Only superusers can see all users
        if request.user.is_superuser:
            return super().get_queryset(request)
        # Regular staff can only see themselves
        return User.objects.filter(id=request.user.id)
    
    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of users unless you're a superuser
        if obj and obj.is_superuser:
            return False  # Cannot delete superusers
        return request.user.is_superuser
    
    def has_change_permission(self, request, obj=None):
        # Users can only edit themselves unless they're superuser
        if not request.user.is_superuser and obj and obj.id != request.user.id:
            return False
        return super().has_change_permission(request, obj)
    
    def has_add_permission(self, request):
        # Only superusers can add users
        return request.user.is_superuser
    
    def delete_model(self, request, obj):
        # Add confirmation and logging for user deletion
        if obj.is_superuser:
            messages.error(request, "Cannot delete superuser accounts!")
            return
        
        # Log the deletion
        messages.warning(request, f"User '{obj.username}' has been deleted by {request.user.username}")
        super().delete_model(request, obj)
    
    def get_form(self, request, obj=None, **kwargs):
        # Restrict form fields for non-superusers
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            # Remove dangerous fields from form
            if 'is_superuser' in form.base_fields:
                del form.base_fields['is_superuser']
            if 'is_staff' in form.base_fields:
                del form.base_fields['is_staff']
            if 'user_permissions' in form.base_fields:
                del form.base_fields['user_permissions']
            if 'groups' in form.base_fields:
                del form.base_fields['groups']
        return form

# Security Enhancement: Restrict Group Admin
class SecureGroupAdmin(BaseGroupAdmin):
    """Custom Group Admin with security restrictions"""
    
    def has_add_permission(self, request):
        # Only superusers can add groups
        return request.user.is_superuser
    
    def has_delete_permission(self, request, obj=None):
        # Only superusers can delete groups
        return request.user.is_superuser
    
    def has_change_permission(self, request, obj=None):
        # Only superusers can change groups
        return request.user.is_superuser

# Unregister default admin classes and register secure ones
admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(User, SecureUserAdmin)
admin.site.register(Group, SecureGroupAdmin)
