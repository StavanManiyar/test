from django.core.management.base import BaseCommand
from django.db import connection
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Optimize database performance with indexes and maintenance'

    def add_arguments(self, parser):
        parser.add_argument(
            '--analyze',
            action='store_true',
            help='Analyze database performance and suggest optimizations',
        )
        parser.add_argument(
            '--create-indexes',
            action='store_true',
            help='Create recommended database indexes',
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🔧 Starting database optimization...')
        )

        if options['analyze']:
            self.analyze_database()

        if options['create_indexes']:
            self.create_indexes()

        # Always run basic maintenance
        self.basic_maintenance()

        self.stdout.write(
            self.style.SUCCESS('✅ Database optimization completed!')
        )

    def analyze_database(self):
        """Analyze database performance"""
        self.stdout.write('📊 Analyzing database performance...')
        
        with connection.cursor() as cursor:
            # Check database size
            if 'postgresql' in connection.settings_dict['ENGINE']:
                cursor.execute("""
                    SELECT pg_size_pretty(pg_database_size(current_database())) as size;
                """)
                size = cursor.fetchone()[0]
                self.stdout.write(f'   Database size: {size}')
                
                # Check table sizes
                cursor.execute("""
                    SELECT 
                        schemaname,
                        tablename,
                        pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size,
                        pg_total_relation_size(schemaname||'.'||tablename) as bytes
                    FROM pg_tables 
                    WHERE schemaname = 'public'
                    ORDER BY bytes DESC
                    LIMIT 10;
                """)
                tables = cursor.fetchall()
                self.stdout.write('   Largest tables:')
                for table in tables:
                    self.stdout.write(f'     {table[1]}: {table[2]}')

            elif 'sqlite' in connection.settings_dict['ENGINE']:
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                self.stdout.write(f'   Total tables: {len(tables)}')

    def create_indexes(self):
        """Create recommended database indexes"""
        self.stdout.write('🗂️  Creating database indexes...')
        
        indexes = [
            # Common indexes for better performance
            "CREATE INDEX IF NOT EXISTS idx_celebration_date ON khschool_celebration(date);",
            "CREATE INDEX IF NOT EXISTS idx_celebration_active ON khschool_celebration(is_active) WHERE is_active = true;",
            "CREATE INDEX IF NOT EXISTS idx_carousel_order ON khschool_carouselimage(\"order\", is_active);",
            "CREATE INDEX IF NOT EXISTS idx_gallery_featured ON khschool_gallery(is_featured) WHERE is_featured = true;",
            "CREATE INDEX IF NOT EXISTS idx_gallery_date ON khschool_gallery(date_created);",
            "CREATE INDEX IF NOT EXISTS idx_gallery_category ON khschool_gallery(category);",
            "CREATE INDEX IF NOT EXISTS idx_galleryimage_order ON khschool_galleryimage(\"order\", gallery_id);",
            "CREATE INDEX IF NOT EXISTS idx_celebration_photos ON khschool_celebrationphoto(celebration_id, \"order\");",
        ]
        
        with connection.cursor() as cursor:
            for index_sql in indexes:
                try:
                    cursor.execute(index_sql)
                    # Extract index name for logging
                    index_name = index_sql.split('IF NOT EXISTS ')[1].split(' ON ')[0]
                    self.stdout.write(f'   ✅ Created index: {index_name}')
                except Exception as e:
                    self.stdout.write(
                        self.style.WARNING(f'   ⚠️  Index creation skipped: {str(e)}')
                    )

    def basic_maintenance(self):
        """Run basic database maintenance"""
        self.stdout.write('🧹 Running database maintenance...')
        
        with connection.cursor() as cursor:
            if 'postgresql' in connection.settings_dict['ENGINE']:
                # PostgreSQL maintenance
                try:
                    cursor.execute("VACUUM ANALYZE;")
                    self.stdout.write('   ✅ VACUUM ANALYZE completed')
                except Exception as e:
                    self.stdout.write(
                        self.style.WARNING(f'   ⚠️  VACUUM failed: {str(e)}')
                    )
            
            elif 'sqlite' in connection.settings_dict['ENGINE']:
                # SQLite maintenance
                try:
                    cursor.execute("VACUUM;")
                    self.stdout.write('   ✅ VACUUM completed')
                    cursor.execute("ANALYZE;")
                    self.stdout.write('   ✅ ANALYZE completed')
                except Exception as e:
                    self.stdout.write(
                        self.style.WARNING(f'   ⚠️  Maintenance failed: {str(e)}')
                    )

        # Django maintenance
        self.stdout.write('🔧 Running Django maintenance...')
        try:
            call_command('clearsessions', verbosity=0)
            self.stdout.write('   ✅ Cleared expired sessions')
        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f'   ⚠️  Session cleanup failed: {str(e)}')
            )
