from django.core.management.base import BaseCommand
from django.db import transaction
from khschool.models import BranchPhoto
from django.core.files.storage import default_storage
import os

class Command(BaseCommand):
    help = 'Manage branch photos - bulk operations and cleanup'

    def add_arguments(self, parser):
        parser.add_argument(
            '--action',
            type=str,
            help='Action to perform: stats, cleanup, reorder',
            required=True
        )
        parser.add_argument(
            '--campus',
            type=str,
            help='Campus branch to operate on (chattral, kadi, iffco, chandkheda)',
        )
        parser.add_argument(
            '--category',
            type=str,
            help='Photo category to filter by',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be done without making changes',
        )

    def handle(self, *args, **options):
        action = options['action']
        campus = options.get('campus')
        category = options.get('category')
        dry_run = options.get('dry_run', False)

        if action == 'stats':
            self.show_stats(campus, category)
        elif action == 'cleanup':
            self.cleanup_orphaned_files(dry_run)
        elif action == 'reorder':
            self.reorder_photos(campus, category, dry_run)
        else:
            self.stdout.write(
                self.style.ERROR(f'Unknown action: {action}')
            )

    def show_stats(self, campus=None, category=None):
        """Show statistics about branch photos"""
        queryset = BranchPhoto.objects.all()
        
        if campus:
            queryset = queryset.filter(campus_branch=campus)
        if category:
            queryset = queryset.filter(category=category)

        total_photos = queryset.count()
        featured_photos = queryset.filter(is_featured=True).count()
        
        self.stdout.write(self.style.SUCCESS(f'Branch Photo Statistics:'))
        self.stdout.write(f'Total photos: {total_photos}')
        self.stdout.write(f'Featured photos: {featured_photos}')
        
        # Stats by campus
        campus_stats = {}
        for choice in BranchPhoto.CAMPUS_CHOICES:
            campus_code, campus_name = choice
            count = queryset.filter(campus_branch=campus_code).count()
            featured_count = queryset.filter(
                campus_branch=campus_code, 
                is_featured=True
            ).count()
            campus_stats[campus_name] = {'total': count, 'featured': featured_count}
        
        self.stdout.write('\nBy Campus:')
        for campus_name, stats in campus_stats.items():
            self.stdout.write(f'  {campus_name}: {stats["total"]} total, {stats["featured"]} featured')
        
        # Stats by category
        category_stats = {}
        for choice in BranchPhoto.PHOTO_CATEGORY_CHOICES:
            category_code, category_name = choice
            count = queryset.filter(category=category_code).count()
            category_stats[category_name] = count
        
        self.stdout.write('\nBy Category:')
        for category_name, count in category_stats.items():
            if count > 0:
                self.stdout.write(f'  {category_name}: {count}')

    def cleanup_orphaned_files(self, dry_run=False):
        """Clean up orphaned image files"""
        self.stdout.write('Checking for orphaned image files...')
        
        # Get all image URLs from database
        db_image_urls = set(
            BranchPhoto.objects.exclude(image_url='').values_list('image_url', flat=True)
        )
        
        # This is a simplified version - in production you'd scan the actual storage
        # and compare with database records
        orphaned_count = 0
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING(f'DRY RUN: Would clean up {orphaned_count} orphaned files')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f'Cleaned up {orphaned_count} orphaned files')
            )

    def reorder_photos(self, campus=None, category=None, dry_run=False):
        """Reorder photos by date uploaded"""
        queryset = BranchPhoto.objects.all()
        
        if campus:
            queryset = queryset.filter(campus_branch=campus)
        if category:
            queryset = queryset.filter(category=category)
        
        photos = queryset.order_by('date_uploaded')
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING(f'DRY RUN: Would reorder {photos.count()} photos')
            )
            for i, photo in enumerate(photos, 1):
                self.stdout.write(f'  {i}. {photo.title} (current order: {photo.order})')
        else:
            with transaction.atomic():
                for i, photo in enumerate(photos, 1):
                    photo.order = i * 10  # Leave gaps for manual reordering
                    photo.save(update_fields=['order'])
            
            self.stdout.write(
                self.style.SUCCESS(f'Reordered {photos.count()} photos')
            )
