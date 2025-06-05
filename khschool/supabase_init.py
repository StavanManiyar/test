from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.dispatch import receiver
import os

from .supabase_storage import initialize_buckets

def init_supabase():
    """Initialize Supabase buckets and other resources"""
    # Check if Supabase credentials are set
    supabase_url = os.environ.get('SUPABASE_URL', '')
    supabase_key = os.environ.get('SUPABASE_KEY', '')
    
    if not supabase_url or not supabase_key:
        print("Supabase credentials not found. Set SUPABASE_URL and SUPABASE_KEY environment variables.")
        return False
    
    # Initialize buckets
    success = initialize_buckets()
    if success:
        print("Supabase storage buckets initialized successfully.")
    else:
        print("Failed to initialize Supabase storage buckets.")
    
    return success

@receiver(post_migrate)
def on_post_migrate(sender, **kwargs):
    """Initialize Supabase after migrations are complete"""
    if sender.name == 'khschool':
        init_supabase()
