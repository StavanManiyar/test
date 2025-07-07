from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings
import os


class Command(BaseCommand):
    help = 'Setup project for VPS deployment'

    def add_arguments(self, parser):
        parser.add_argument(
            '--create-superuser',
            action='store_true',
            help='Create a superuser after setup',
        )
        parser.add_argument(
            '--collect-static',
            action='store_true',
            help='Collect static files after setup',
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🚀 Setting up Kapadia School for VPS deployment...')
        )

        # Check if we're in production
        is_production = not settings.DEBUG
        if is_production:
            self.stdout.write(
                self.style.WARNING('⚠️  Running in PRODUCTION mode')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS('🔧 Running in DEVELOPMENT mode')
            )

        # Step 1: Create directories
        self.stdout.write('📁 Creating necessary directories...')
        directories = [
            'gallery/festival/images',
            'gallery/festival/gallery',
            'gallery/carousel/images',
            'gallery/thumbnails',
            'logs',
        ]
        
        for directory in directories:
            dir_path = os.path.join(settings.BASE_DIR, directory)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
                self.stdout.write(f'   ✅ Created: {directory}')
            else:
                self.stdout.write(f'   📁 Exists: {directory}')

        # Step 2: Run migrations
        self.stdout.write('🗄️  Running database migrations...')
        try:
            call_command('makemigrations', verbosity=0)
            call_command('migrate', verbosity=0)
            self.stdout.write('   ✅ Migrations completed successfully')
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'   ❌ Migration failed: {str(e)}')
            )

        # Step 3: Collect static files (if requested)
        if options['collect_static']:
            self.stdout.write('📦 Collecting static files...')
            try:
                call_command('collectstatic', '--noinput', verbosity=0)
                self.stdout.write('   ✅ Static files collected successfully')
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'   ❌ Static collection failed: {str(e)}')
                )

        # Step 4: Test database connection
        self.stdout.write('🔗 Testing database connection...')
        try:
            from django.db import connection
            cursor = connection.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            if result:
                self.stdout.write('   ✅ Database connection successful')
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'   ❌ Database connection failed: {str(e)}')
            )

        # Step 5: Test Supabase connection (if configured)
        self.stdout.write('☁️  Testing Supabase connection...')
        if hasattr(settings, 'SUPABASE_URL') and settings.SUPABASE_URL:
            try:
                from khschool.supabase_init import supabase_client
                # Simple test to see if we can connect
                response = supabase_client.table('_test').select('*').limit(1).execute()
                self.stdout.write('   ✅ Supabase connection successful')
            except Exception as e:
                self.stdout.write(
                    self.style.WARNING(f'   ⚠️  Supabase connection test failed: {str(e)}')
                )
                self.stdout.write('      This is normal if Supabase is not configured yet')
        else:
            self.stdout.write('   ⚠️  Supabase not configured (SUPABASE_URL not set)')

        # Step 6: Check required environment variables
        self.stdout.write('🔧 Checking environment variables...')
        required_vars = ['SECRET_KEY']
        optional_vars = ['DATABASE_URL', 'SUPABASE_URL', 'SUPABASE_KEY', 'VPS_SERVER_IP']
        
        for var in required_vars:
            try:
                value = getattr(settings, var, None)
                if value and value.strip():  # Check if not empty
                    self.stdout.write(f'   ✅ {var}: Configured')
                else:
                    self.stdout.write(
                        self.style.ERROR(f'   ❌ {var}: Missing or empty (REQUIRED)')
                    )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'   ❌ {var}: Error checking - {str(e)}')
                )
        
        for var in optional_vars:
            try:
                value = getattr(settings, var, None)
                if value and value.strip():  # Check if not empty
                    self.stdout.write(f'   ✅ {var}: Configured')
                else:
                    self.stdout.write(f'   ⚠️  {var}: Not configured (optional)')
            except Exception:
                self.stdout.write(f'   ⚠️  {var}: Not configured (optional)')

        # Step 7: Create superuser (if requested)
        if options['create_superuser']:
            self.stdout.write('👤 Creating superuser...')
            try:
                call_command('createsuperuser')
                self.stdout.write('   ✅ Superuser created successfully')
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'   ❌ Superuser creation failed: {str(e)}')
                )

        # Step 8: Final checks
        self.stdout.write('🔍 Running Django system checks...')
        try:
            call_command('check', verbosity=0)
            self.stdout.write('   ✅ All system checks passed')
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'   ❌ System checks failed: {str(e)}')
            )

        # Summary
        self.stdout.write('')
        self.stdout.write(
            self.style.SUCCESS('🎉 VPS setup completed!')
        )
        self.stdout.write('')
        self.stdout.write('Next steps:')
        self.stdout.write('1. Configure environment variables in .env file')
        self.stdout.write('2. Set up Nginx configuration (copy nginx.conf)')
        self.stdout.write('3. Set up Supervisor configuration (copy supervisor.conf)')
        self.stdout.write('4. Configure SSL certificates with Let\'s Encrypt')
        self.stdout.write('5. Test your deployment')
        self.stdout.write('')
        self.stdout.write('For detailed instructions, see:')
        self.stdout.write('- README.md')
        self.stdout.write('- VPS_HOSTINGER_DEPLOYMENT_GUIDE.md')
        self.stdout.write('')
        self.stdout.write(
            self.style.SUCCESS('Good luck with your deployment! 🚀')
        )
