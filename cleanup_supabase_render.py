#!/usr/bin/env python3
"""
Cleanup script to remove Supabase and Render dependencies for VPS-only deployment
"""

import os
import shutil
from pathlib import Path

# Files to remove completely
FILES_TO_REMOVE = [
    'khschool/supabase_init.py',
    'khschool/supabase_storage.py', 
    'khschool/models_supabase.py',
    'khschool/fields.py',  # Contains Supabase fields
    'render.yaml',
    'config/render.yaml',
    'Procfile',
    'RENDER_DEPLOYMENT_GUIDE.md',
    'SUPABASE_SETUP.md',
    'runtime.txt',
]

# Directories to remove
DIRS_TO_REMOVE = [
    'archive/.env.production',
]

# Dependencies to remove from requirements.txt
DEPENDENCIES_TO_REMOVE = [
    'supabase==1.2.0',
    '# supabase==1.2.0',
    'sentry-sdk==1.40.0',  # Optional monitoring service
    'django-cors-headers==4.3.1',  # Not needed for VPS deployment
]

def remove_files():
    """Remove unnecessary files"""
    print("🗑️ Removing Supabase and Render files...")
    
    for file_path in FILES_TO_REMOVE:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"  ✅ Removed: {file_path}")
        else:
            print(f"  ⚠️ Not found: {file_path}")
    
    print("\n📁 Removing directories...")
    for dir_path in DIRS_TO_REMOVE:
        if os.path.exists(dir_path):
            if os.path.isfile(dir_path):
                os.remove(dir_path)
            else:
                shutil.rmtree(dir_path)
            print(f"  ✅ Removed: {dir_path}")

def clean_requirements():
    """Remove Supabase and other cloud-specific dependencies from requirements.txt"""
    print("\n📦 Cleaning requirements.txt...")
    
    if not os.path.exists('requirements.txt'):
        print("  ⚠️ requirements.txt not found")
        return
    
    with open('requirements.txt', 'r') as f:
        lines = f.readlines()
    
    # Filter out unwanted dependencies
    clean_lines = []
    for line in lines:
        line = line.strip()
        should_remove = False
        
        for dep_to_remove in DEPENDENCIES_TO_REMOVE:
            if dep_to_remove.lower() in line.lower():
                should_remove = True
                print(f"  ❌ Removing: {line}")
                break
        
        if not should_remove and line:
            clean_lines.append(line + '\n')
    
    # Write cleaned requirements
    with open('requirements.txt', 'w') as f:
        f.writelines(clean_lines)
    
    print("  ✅ requirements.txt cleaned")

def update_env_example():
    """Update .env.example to remove Supabase variables"""
    print("\n📝 Updating .env.example...")
    
    if os.path.exists('.env.example'):
        with open('.env.example', 'r') as f:
            content = f.read()
        
        # Remove Supabase-related environment variables
        lines = content.split('\n')
        clean_lines = []
        skip_supabase = False
        
        for line in lines:
            if 'SUPABASE' in line.upper() or 'RENDER' in line.upper():
                print(f"  ❌ Removing: {line}")
            else:
                clean_lines.append(line)
        
        with open('.env.example', 'w') as f:
            f.write('\n'.join(clean_lines))
        
        print("  ✅ .env.example updated")

def clean_models_imports():
    """Remove Supabase imports from models.py"""
    print("\n🔧 Cleaning models.py...")
    
    models_file = 'khschool/models.py'
    if not os.path.exists(models_file):
        print("  ⚠️ models.py not found")
        return
    
    with open(models_file, 'r') as f:
        content = f.read()
    
    # Remove Supabase-related imports and references
    lines = content.split('\n')
    clean_lines = []
    
    for line in lines:
        if any(keyword in line for keyword in ['supabase', 'fields.py', 'CarouselImageField', 'CelebrationImageField', 'GalleryImageField']):
            print(f"  ❌ Removing: {line.strip()}")
        else:
            clean_lines.append(line)
    
    with open(models_file, 'w') as f:
        f.write('\n'.join(clean_lines))
    
    print("  ✅ models.py cleaned")

def clean_settings():
    """Remove Supabase references from settings.py"""
    print("\n⚙️ Cleaning settings.py...")
    
    settings_file = 'kapadiaschool/settings.py'
    if not os.path.exists(settings_file):
        print("  ⚠️ settings.py not found")
        return
    
    with open(settings_file, 'r') as f:
        content = f.read()
    
    # Remove Supabase configuration
    lines = content.split('\n')
    clean_lines = []
    skip_supabase_section = False
    
    for line in lines:
        if 'SUPABASE' in line.upper() and '=' in line:
            print(f"  ❌ Removing: {line.strip()}")
            skip_supabase_section = True
        elif skip_supabase_section and line.strip() == '':
            skip_supabase_section = False
            clean_lines.append(line)
        elif not skip_supabase_section:
            clean_lines.append(line)
    
    with open(settings_file, 'w') as f:
        f.write('\n'.join(clean_lines))
    
    print("  ✅ settings.py cleaned")

def create_vps_requirements():
    """Create a clean requirements.txt optimized for VPS deployment"""
    print("\n📦 Creating VPS-optimized requirements.txt...")
    
    vps_requirements = """# Core Django
Django==5.2.1
asgiref==3.8.1
sqlparse==0.5.3
tzdata==2024.2

# Production Server
gunicorn==21.2.0
whitenoise==6.6.0

# Database
dj-database-url==2.1.0
psycopg2-binary==2.9.10

# Environment & Configuration
python-dotenv==1.0.1
python-decouple==3.8

# Image Processing
Pillow==10.0.0

# External Services
requests==2.31.0

# Utilities
python-slugify==8.0.1

# Background Tasks & Caching (Optional for VPS)
celery==5.3.0
redis==4.5.5

# Development & Testing (optional)
django-debug-toolbar==4.2.0
pytest-django==4.7.0
coverage==7.4.0
"""
    
    with open('requirements.txt', 'w') as f:
        f.write(vps_requirements)
    
    print("  ✅ VPS-optimized requirements.txt created")

def main():
    """Main cleanup function"""
    print("🧹 Starting Supabase and Render cleanup for VPS deployment...")
    print("=" * 60)
    
    # Change to project directory
    os.chdir(Path(__file__).parent)
    
    # Perform cleanup
    remove_files()
    clean_requirements()
    update_env_example() 
    clean_models_imports()
    clean_settings()
    create_vps_requirements()
    
    print("\n" + "=" * 60)
    print("✅ Cleanup completed successfully!")
    print("\n📋 Next steps:")
    print("  1. Review the cleaned files")
    print("  2. Run: python manage.py makemigrations")
    print("  3. Run: python manage.py migrate")
    print("  4. Test your application locally")
    print("  5. Deploy to your VPS using ./scripts/deploy_vps.sh")
    print("\n🚀 Your project is now VPS-ready!")

if __name__ == "__main__":
    main()
