from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Checks database connection and configuration'

    def handle(self, *args, **options):
        self.stdout.write('Checking database connection...')
        
        try:
            db_conn = connections['default']
            db_conn.cursor()
            self.stdout.write(self.style.SUCCESS('Database connection successful!'))
            
            # Print information about the connection
            self.stdout.write(f"Database engine: {connections.databases['default']['ENGINE']}")
            
            if connections.databases['default']['ENGINE'] == 'django.db.backends.sqlite3':
                db_path = connections.databases['default']['NAME']
                self.stdout.write(f"SQLite database path: {db_path}")
                self.stdout.write(f"Database file exists: {os.path.exists(db_path)}")
                self.stdout.write(f"Database file size: {os.path.getsize(db_path) if os.path.exists(db_path) else 0} bytes")
            else:
                self.stdout.write(f"Database name: {connections.databases['default']['NAME']}")
                self.stdout.write(f"Database host: {connections.databases['default'].get('HOST', 'Not specified')}")
            
        except OperationalError as e:
            self.stdout.write(self.style.ERROR(f'Database connection failed! Error: {e}')) 