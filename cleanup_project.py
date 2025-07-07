#!/usr/bin/env python3
"""
Project Cleanup and Organization Script
Organizes Kapadia High School Django project files into proper structure
"""

import os
import shutil
from pathlib import Path

def create_directories():
    """Create organized directory structure"""
    directories = [
        'docs',
        'scripts', 
        'config',
        'tests',
        'archive'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created directory: {directory}/")

def organize_documentation():
    """Move all documentation files to docs/ directory"""
    doc_files = [
        'README.md',
        'PROJECT_INDEX.md',
        'DEPLOYMENT_GUIDE.md',
        'INSTALLATION_SUMMARY.md',
        'MAINTENANCE_GUIDE.md', 
        'VPS_HOSTINGER_DEPLOYMENT_GUIDE.md',
        'RENDER_DEPLOYMENT_GUIDE.md',
        'SUPABASE_SETUP.md',
        'IMAGE_UPLOAD_GUIDE.md',
        'VPS.md'
    ]
    
    print("\n📚 Organizing documentation files...")
    for doc_file in doc_files:
        if os.path.exists(doc_file):
            shutil.move(doc_file, f'docs/{doc_file}')
            print(f"📝 Moved {doc_file} → docs/")

def organize_scripts():
    """Move all script files to scripts/ directory"""
    script_files = [
        'deploy.sh',
        'deploy_vps.sh', 
        'build.sh',
        'backup_script.sh',
        'health_check.sh',
        'update_app.sh',
        'setup_cron.sh',
        'test_domains.sh',
        'make_scripts_executable.sh'
    ]
    
    print("\n🔧 Organizing script files...")
    for script_file in script_files:
        if os.path.exists(script_file):
            shutil.move(script_file, f'scripts/{script_file}')
            print(f"📜 Moved {script_file} → scripts/")

def organize_config():
    """Move configuration files to config/ directory"""
    config_files = [
        'render.yaml',
        'requirements.txt',
        'runtime.txt'
    ]
    
    print("\n⚙️ Organizing configuration files...")
    for config_file in config_files:
        if os.path.exists(config_file):
            shutil.copy2(config_file, f'config/{config_file}')
            print(f"⚙️ Copied {config_file} → config/ (keeping original)")

def organize_tests():
    """Move test files to tests/ directory"""
    test_files = [
        'test_db.py'
    ]
    
    print("\n🧪 Organizing test files...")
    for test_file in test_files:
        if os.path.exists(test_file):
            shutil.move(test_file, f'tests/{test_file}')
            print(f"🧪 Moved {test_file} → tests/")

def archive_old_files():
    """Archive outdated/duplicate files"""
    old_files = [
        'gallery_new.html',
        'image_test.html',
        '.env.production'
    ]
    
    print("\n🗄️ Archiving old/duplicate files...")
    for old_file in old_files:
        if os.path.exists(old_file):
            shutil.move(old_file, f'archive/{old_file}')
            print(f"🗄️ Archived {old_file} → archive/")
        elif os.path.exists(f'templates/{old_file}'):
            shutil.move(f'templates/{old_file}', f'archive/{old_file}')
            print(f"🗄️ Archived templates/{old_file} → archive/")

def create_main_readme():
    """Create a main README.md that references the organized docs"""
    readme_content = """# 🏫 Kapadia High School Website

A modern Django-based website for Kapadia High School with multi-campus management and photo gallery system.

## 🚀 Quick Start

```bash
# 1. Clone and setup
git clone <your-repo>
cd kapadiaschool
pip install -r requirements.txt

# 2. Database setup
python manage.py migrate
python manage.py createsuperuser

# 3. Run development server
python manage.py runserver
```

## 📚 Documentation

All detailed documentation is in the `docs/` folder:

- **[📋 Complete Project Index](docs/PROJECT_INDEX.md)** - Overview of all files and features
- **[🚀 Deployment Guide](docs/DEPLOYMENT_GUIDE.md)** - Complete deployment instructions
- **[🖼️ Image Upload Guide](docs/IMAGE_UPLOAD_GUIDE.md)** - How to manage photos
- **[🔧 Maintenance Guide](docs/MAINTENANCE_GUIDE.md)** - Ongoing maintenance tasks

## 🏫 Features

✅ **Multi-Campus Management** - 4 campus locations
✅ **Photo Gallery System** - Campus-specific photo galleries  
✅ **Admin Panel** - Easy content management
✅ **Mobile Responsive** - Works on all devices
✅ **VPS Deployment Ready** - Production deployment scripts
✅ **User Role Management** - Different access levels

## 🖥️ Deployment

```bash
# VPS Deployment
cd scripts/
./deploy.sh

# Cloud Deployment (Render.com)
# Uses config/render.yaml automatically
```

## 📞 Support

- **Scripts**: Check `scripts/` folder for deployment and maintenance
- **Configuration**: Check `config/` folder for deployment configs
- **Documentation**: Check `docs/` folder for detailed guides

## 🎯 Project Status: Production Ready ✅

Last Updated: {current_date}
"""
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print("📄 Created main README.md")

def update_script_paths():
    """Update script references to point to new locations"""
    print("\n🔄 Updating script path references...")
    
    # Update main deployment guide
    if os.path.exists('docs/DEPLOYMENT_GUIDE.md'):
        with open('docs/DEPLOYMENT_GUIDE.md', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update script paths
        content = content.replace('./deploy.sh', './scripts/deploy.sh')
        content = content.replace('./health_check.sh', './scripts/health_check.sh')
        content = content.replace('./backup_script.sh', './scripts/backup_script.sh')
        
        with open('docs/DEPLOYMENT_GUIDE.md', 'w', encoding='utf-8') as f:
            f.write(content)
        print("📝 Updated deployment guide script paths")

def create_scripts_readme():
    """Create README for scripts directory"""
    scripts_readme = """# 🔧 Deployment and Maintenance Scripts

## 🚀 Deployment Scripts

- **`deploy.sh`** - Main VPS deployment script
- **`deploy_vps.sh`** - Alternative VPS deployment
- **`build.sh`** - Build process for production

## 🔧 Maintenance Scripts

- **`backup_script.sh`** - Database backup automation
- **`health_check.sh`** - System health monitoring
- **`update_app.sh`** - Application update process
- **`setup_cron.sh`** - Setup scheduled tasks

## 🧪 Testing Scripts

- **`test_domains.sh`** - Domain connectivity testing
- **`make_scripts_executable.sh`** - Make all scripts executable

## 📋 Usage

```bash
# Make scripts executable
chmod +x scripts/*.sh

# Deploy to VPS
./scripts/deploy.sh

# Check system health
./scripts/health_check.sh

# Backup database
./scripts/backup_script.sh
```

## ⚠️ Important Notes

1. **Update VPS details** in deploy.sh before running
2. **Test locally** before deploying to production
3. **Backup database** before major updates
"""
    
    with open('scripts/README.md', 'w', encoding='utf-8') as f:
        f.write(scripts_readme)
    print("📄 Created scripts/README.md")

def main():
    """Run the complete cleanup and organization process"""
    print("🧹 Starting Kapadia High School Project Cleanup...")
    print("=" * 60)
    
    # Create organized directory structure
    create_directories()
    
    # Organize files by type
    organize_documentation()
    organize_scripts() 
    organize_config()
    organize_tests()
    archive_old_files()
    
    # Create helpful documentation
    create_main_readme()
    create_scripts_readme()
    
    # Update references
    update_script_paths()
    
    print("\n" + "=" * 60)
    print("🎉 Project cleanup completed successfully!")
    print("\n📁 New Project Structure:")
    print("""
kapadiaschool/
├── 📚 docs/           # All documentation
├── 🔧 scripts/        # Deployment & maintenance scripts  
├── ⚙️ config/         # Configuration files
├── 🧪 tests/          # Test files
├── 🗄️ archive/        # Old/duplicate files
├── 🐍 Django core files (unchanged)
├── 🎨 templates/ (unchanged)
└── 🎨 static/ (unchanged)
""")
    
    print("\n📋 Next Steps:")
    print("1. Review organized files in each directory")
    print("2. Update VPS details in scripts/deploy.sh")
    print("3. Test the campus gallery system locally")
    print("4. Deploy to production using scripts/deploy.sh")
    print("\n✅ Your project is now properly organized and production-ready!")

if __name__ == "__main__":
    main()
