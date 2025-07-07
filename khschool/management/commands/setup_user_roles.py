from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from khschool.models import Celebration, CelebrationPhoto, Gallery, GalleryImage, CarouselImage


class Command(BaseCommand):
    help = 'Set up user roles and permissions for the school management system'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Setting up user roles and permissions...'))
        
        # Create user groups
        self.create_groups()
        
        # Assign permissions to groups
        self.assign_permissions()
        
        self.stdout.write(self.style.SUCCESS('User roles and permissions setup completed!'))

    def create_groups(self):
        """Create user groups for different access levels"""
        
        # 1. Content Managers - Can add/edit content but not delete or change critical settings
        content_manager_group, created = Group.objects.get_or_create(name='Content Managers')
        if created:
            self.stdout.write(f'Created group: {content_manager_group.name}')
        
        # 2. Gallery Editors - Can only manage gallery images
        gallery_editor_group, created = Group.objects.get_or_create(name='Gallery Editors')
        if created:
            self.stdout.write(f'Created group: {gallery_editor_group.name}')
        
        # 3. Event Coordinators - Can manage celebrations and events
        event_coordinator_group, created = Group.objects.get_or_create(name='Event Coordinators')
        if created:
            self.stdout.write(f'Created group: {event_coordinator_group.name}')
        
        # 4. Read Only Users - Can only view admin but not edit
        readonly_group, created = Group.objects.get_or_create(name='Read Only Users')
        if created:
            self.stdout.write(f'Created group: {readonly_group.name}')

    def assign_permissions(self):
        """Assign specific permissions to each group"""
        
        # Get groups
        content_managers = Group.objects.get(name='Content Managers')
        gallery_editors = Group.objects.get(name='Gallery Editors')
        event_coordinators = Group.objects.get(name='Event Coordinators')
        readonly_users = Group.objects.get(name='Read Only Users')
        
        # Get content types for our models
        celebration_ct = ContentType.objects.get_for_model(Celebration)
        celebration_photo_ct = ContentType.objects.get_for_model(CelebrationPhoto)
        gallery_ct = ContentType.objects.get_for_model(Gallery)
        gallery_image_ct = ContentType.objects.get_for_model(GalleryImage)
        carousel_ct = ContentType.objects.get_for_model(CarouselImage)
        
        # Content Managers - Can add/change content but not delete
        content_manager_permissions = [
            # Celebrations
            Permission.objects.get(codename='add_celebration', content_type=celebration_ct),
            Permission.objects.get(codename='change_celebration', content_type=celebration_ct),
            Permission.objects.get(codename='view_celebration', content_type=celebration_ct),
            
            # Celebration Photos
            Permission.objects.get(codename='add_celebrationphoto', content_type=celebration_photo_ct),
            Permission.objects.get(codename='change_celebrationphoto', content_type=celebration_photo_ct),
            Permission.objects.get(codename='view_celebrationphoto', content_type=celebration_photo_ct),
            
            # Gallery
            Permission.objects.get(codename='add_gallery', content_type=gallery_ct),
            Permission.objects.get(codename='change_gallery', content_type=gallery_ct),
            Permission.objects.get(codename='view_gallery', content_type=gallery_ct),
            
            # Gallery Images
            Permission.objects.get(codename='add_galleryimage', content_type=gallery_image_ct),
            Permission.objects.get(codename='change_galleryimage', content_type=gallery_image_ct),
            Permission.objects.get(codename='view_galleryimage', content_type=gallery_image_ct),
            
            # Carousel (limited access)
            Permission.objects.get(codename='change_carouselimage', content_type=carousel_ct),
            Permission.objects.get(codename='view_carouselimage', content_type=carousel_ct),
        ]
        content_managers.permissions.set(content_manager_permissions)
        self.stdout.write('Assigned permissions to Content Managers')
        
        # Gallery Editors - Only gallery and image management
        gallery_editor_permissions = [
            # Gallery only
            Permission.objects.get(codename='add_gallery', content_type=gallery_ct),
            Permission.objects.get(codename='change_gallery', content_type=gallery_ct),
            Permission.objects.get(codename='view_gallery', content_type=gallery_ct),
            
            # Gallery Images only
            Permission.objects.get(codename='add_galleryimage', content_type=gallery_image_ct),
            Permission.objects.get(codename='change_galleryimage', content_type=gallery_image_ct),
            Permission.objects.get(codename='view_galleryimage', content_type=gallery_image_ct),
            Permission.objects.get(codename='delete_galleryimage', content_type=gallery_image_ct),
        ]
        gallery_editors.permissions.set(gallery_editor_permissions)
        self.stdout.write('Assigned permissions to Gallery Editors')
        
        # Event Coordinators - Only celebrations and events
        event_coordinator_permissions = [
            # Celebrations
            Permission.objects.get(codename='add_celebration', content_type=celebration_ct),
            Permission.objects.get(codename='change_celebration', content_type=celebration_ct),
            Permission.objects.get(codename='view_celebration', content_type=celebration_ct),
            
            # Celebration Photos
            Permission.objects.get(codename='add_celebrationphoto', content_type=celebration_photo_ct),
            Permission.objects.get(codename='change_celebrationphoto', content_type=celebration_photo_ct),
            Permission.objects.get(codename='view_celebrationphoto', content_type=celebration_photo_ct),
            Permission.objects.get(codename='delete_celebrationphoto', content_type=celebration_photo_ct),
        ]
        event_coordinators.permissions.set(event_coordinator_permissions)
        self.stdout.write('Assigned permissions to Event Coordinators')
        
        # Read Only Users - Only view permissions
        readonly_permissions = [
            Permission.objects.get(codename='view_celebration', content_type=celebration_ct),
            Permission.objects.get(codename='view_celebrationphoto', content_type=celebration_photo_ct),
            Permission.objects.get(codename='view_gallery', content_type=gallery_ct),
            Permission.objects.get(codename='view_galleryimage', content_type=gallery_image_ct),
            Permission.objects.get(codename='view_carouselimage', content_type=carousel_ct),
        ]
        readonly_users.permissions.set(readonly_permissions)
        self.stdout.write('Assigned permissions to Read Only Users')

    def add_arguments(self, parser):
        parser.add_argument(
            '--create-demo-users',
            action='store_true',
            help='Create demo users for each group',
        )
        
        if self.options.get('create_demo_users'):
            self.create_demo_users()

    def create_demo_users(self):
        """Create demo users for testing different access levels"""
        
        # Get groups
        content_managers = Group.objects.get(name='Content Managers')
        gallery_editors = Group.objects.get(name='Gallery Editors')
        event_coordinators = Group.objects.get(name='Event Coordinators')
        readonly_users = Group.objects.get(name='Read Only Users')
        
        # Create users and assign to groups
        users_to_create = [
            ('content_manager', 'content@kapadiaschool.com', 'Content Manager User', content_managers),
            ('gallery_editor', 'gallery@kapadiaschool.com', 'Gallery Editor User', gallery_editors),
            ('event_coordinator', 'events@kapadiaschool.com', 'Event Coordinator User', event_coordinators),
            ('readonly_user', 'readonly@kapadiaschool.com', 'Read Only User', readonly_users),
        ]
        
        for username, email, full_name, group in users_to_create:
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password='demo123',  # Change this in production
                    first_name=full_name.split()[0],
                    last_name=' '.join(full_name.split()[1:]),
                    is_staff=True  # Allow admin access
                )
                user.groups.add(group)
                self.stdout.write(f'Created user: {username} in group: {group.name}')
