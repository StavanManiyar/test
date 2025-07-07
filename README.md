# 🏫 Kapadia High School Website

A comprehensive Django-based website for Kapadia High School featuring multi-campus management, photo gallery systems, and modern web technologies. Built for scalability with multiple deployment options including VPS, Render, and Supabase integration.

## 📋 Project Overview

- **Framework**: Django 5.2.1
- **Database**: PostgreSQL (Production) / SQLite (Development)
- **Frontend**: HTML5, CSS3, JavaScript
- **Storage**: Local File System + Optional Supabase Cloud Storage
- **Deployment**: VPS (Self-hosted) / Render.com / Cloud platforms
- **Features**: Multi-campus management, Gallery system, Admin panel, User roles

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip
- Git
- Virtual environment (recommended)

### Local Development Setup

```bash
# 1. Clone the repository
git clone your-repo-url
cd kapadiaschool

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Environment setup
cp .env.example .env
# Edit .env with your configuration

# 5. Database setup
python manage.py migrate
python manage.py createsuperuser

# 6. Create sample data (optional)
python manage.py setup_user_roles

# 7. Run development server
python manage.py runserver
```

### Access the Application
- **Website**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **Campus Pages**: 
  - http://127.0.0.1:8000/chattral/
  - http://127.0.0.1:8000/kadi/
  - http://127.0.0.1:8000/iffco/
  - http://127.0.0.1:8000/chandkheda/

## 🏫 Key Features

### ✅ Multi-Campus Management
- **4 Campus Locations**: Chattral, Kadi, IFFCO, Chandkheda
- **Campus-Specific Pages**: Individual pages for each campus
- **Featured Photos**: 4-5 preview photos on each campus page
- **Full Gallery**: Dedicated gallery pages for each campus

### ✅ Advanced Photo Gallery System
- **Gallery Categories**: Festival, Academic, Sports, Cultural, Events
- **Campus Branch Filtering**: Organize photos by campus location
- **Featured Gallery**: Homepage showcase of selected galleries
- **Lightbox Viewer**: Professional photo viewing experience
- **Mobile Responsive**: Perfect display on all devices

### ✅ Content Management System
- **Django Admin Panel**: User-friendly content management
- **Bulk Actions**: Manage multiple items simultaneously
- **Visual Previews**: Thumbnail displays in admin
- **Role-Based Access**: Different permission levels
- **Image Optimization**: Automatic image processing

### ✅ Modern Web Technologies
- **Responsive Design**: Mobile-first approach
- **Performance Optimized**: Caching and database optimization
- **SEO Friendly**: Search engine optimized
- **Security Features**: Built-in Django security
- **Static File Management**: WhiteNoise integration

## 📁 Project Structure

```
kapadiaschool/
├── 🐍 CORE DJANGO FILES
│   ├── manage.py                     # Django management script
│   ├── kapadiaschool/               # Main project directory
│   │   ├── settings.py              # Configuration
│   │   ├── urls.py                  # URL routing
│   │   ├── wsgi.py & asgi.py        # Server interfaces
│   └── khschool/                    # Main application
│       ├── models.py                # Database models
│       ├── views.py                 # View functions
│       ├── admin.py                 # Admin interface
│       ├── urls.py                  # App URLs
│       ├── migrations/              # Database migrations
│       ├── management/commands/     # Custom commands
│       └── templatetags/            # Template filters
│
├── 🎨 FRONTEND FILES
│   ├── templates/                   # HTML templates
│   │   ├── base.html               # Base template
│   │   ├── home.html               # Homepage
│   │   ├── campus pages            # Campus-specific pages
│   │   └── gallery.html            # Photo gallery
│   └── static/                      # CSS, JS, Images
│       ├── css/                    # Stylesheets
│       ├── js/                     # JavaScript files
│       ├── images/                 # Static images
│       └── documents/              # PDF documents
│
├── 🚀 DEPLOYMENT & SCRIPTS
│   ├── scripts/                     # Deployment scripts
│   │   ├── deploy.sh               # Main VPS deployment
│   │   ├── build.sh                # Build process
│   │   ├── backup_script.sh        # Database backup
│   │   ├── health_check.sh         # System monitoring
│   │   └── update_app.sh           # App updates
│   ├── requirements.txt             # Python dependencies
│   ├── render.yaml                  # Render.com config
│   └── .env.example                # Environment template
│
├── 📚 DOCUMENTATION
│   └── docs/                        # Complete documentation
│       ├── PROJECT_INDEX.md        # Project overview
│       ├── DEPLOYMENT_GUIDE.md     # Deployment instructions
│       ├── IMAGE_UPLOAD_GUIDE.md   # Photo management
│       ├── MAINTENANCE_GUIDE.md    # Ongoing maintenance
│       └── SUPABASE_SETUP.md       # Cloud storage setup
│
└── 📊 DATA & MEDIA
    ├── gallery/                     # Image storage
    │   ├── festival/               # Event photos
    │   ├── carousel/               # Homepage slider
    │   └── branch_photos/          # Campus photos
    └── logs/                        # Application logs
```

## 🖥️ Deployment Options

### Option 1: VPS Deployment (Recommended for Production)

**Prerequisites:**
- Ubuntu/Debian VPS with root access
- Domain pointing to your VPS IP
- SSH access to your server

**Deployment Steps:**

```bash
# 1. Configure deployment script
cd scripts/
nano deploy.sh
# Update: VPS_USER, VPS_HOST, DOMAIN

# 2. Run deployment
chmod +x deploy.sh
./deploy.sh

# 3. Monitor deployment
./health_check.sh
```

**What the script does:**
- ✅ Sets up Python environment
- ✅ Installs dependencies
- ✅ Configures PostgreSQL database
- ✅ Sets up Nginx web server
- ✅ Creates systemd service
- ✅ Configures SSL (optional)
- ✅ Creates superuser account
- ✅ Sets up sample galleries

### Option 2: Render Deployment (Easy Cloud Hosting)

**Steps:**

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Connect to Render:**
   - Sign up at [Render.com](https://render.com)
   - Connect your GitHub repository
   - Render automatically detects `render.yaml`

3. **Environment Variables:**
   Set in Render dashboard:
   ```bash
   SECRET_KEY=your-secret-key
   DEBUG=False
   DATABASE_URL=postgresql://... (auto-provided)
   ```

4. **Post-deployment:**
   ```bash
   # Access Render shell and create superuser
   python manage.py createsuperuser
   ```

**Render Benefits:**
- ✅ Automatic deployments from GitHub
- ✅ Managed PostgreSQL database
- ✅ Free SSL certificates
- ✅ Auto-scaling capabilities
- ✅ Built-in monitoring

### Option 3: Supabase Integration (Cloud Storage)

**Setup Steps:**

1. **Create Supabase Project:**
   - Sign up at [Supabase.com](https://supabase.com)
   - Create new project
   - Get API URL and anon key

2. **Configure Environment:**
   ```bash
   # Add to .env or Render environment
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_anon_key
   ```

3. **Initialize Storage:**
   ```bash
   python initialize_supabase.py
   ```

**Supabase Benefits:**
- ✅ Cloud image storage
- ✅ CDN delivery
- ✅ Automatic backups
- ✅ Scalable storage
- ✅ Real-time capabilities

## 🔧 Administrative Tasks

### Adding Campus Photos

1. **Access Admin Panel:** `/admin`
2. **Create Gallery:**
   - Go to "Galleries" → "Add Gallery"
   - Select Campus Branch
   - Check "Show on Campus Page" for featured photos
3. **Add Images:**
   - Upload photos to the gallery
   - Set display order and captions
   - Photos appear automatically on campus pages

### User Management

```bash
# Setup user roles
python manage.py setup_user_roles

# Create additional users
python manage.py createsuperuser

# Check database status
python manage.py check_db
```

### Maintenance Commands

```bash
# Database optimization
python manage.py optimize_db

# Backup database
./scripts/backup_script.sh

# Update application
./scripts/update_app.sh

# Health check
./scripts/health_check.sh
```

## 📚 Complete Documentation

### Core Documentation
- **[📋 Complete Project Index](docs/PROJECT_INDEX.md)** - Detailed file structure and features
- **[🚀 Deployment Guide](docs/DEPLOYMENT_GUIDE.md)** - Step-by-step deployment instructions
- **[🖼️ Image Upload Guide](docs/IMAGE_UPLOAD_GUIDE.md)** - Photo management workflows
- **[🔧 Maintenance Guide](docs/MAINTENANCE_GUIDE.md)** - Ongoing maintenance tasks

### Integration Guides
- **[☁️ Supabase Setup Guide](docs/SUPABASE_SETUP.md)** - Cloud storage integration
- **[🖥️ VPS Deployment Guide](docs/VPS_HOSTINGER_DEPLOYMENT_GUIDE.md)** - VPS hosting setup
- **[📊 Installation Summary](docs/INSTALLATION_SUMMARY.md)** - Quick setup reference

### Additional Resources
- **[📈 Performance Optimization](OPTIMIZATION_SUMMARY.md)** - Speed improvements
- **[🧹 Cleanup Summary](VPS_CLEANUP_SUMMARY.md)** - Maintenance procedures
- **[📝 Final Project Summary](FINAL_PROJECT_SUMMARY.md)** - Complete feature overview

## 🛠️ Technology Stack

### Backend
- **Django 5.2.1** - Web framework
- **Python 3.8+** - Programming language
- **PostgreSQL** - Production database
- **SQLite** - Development database
- **Gunicorn** - WSGI server
- **WhiteNoise** - Static file serving

### Frontend
- **HTML5 & CSS3** - Modern web standards
- **JavaScript** - Interactive features
- **Bootstrap Components** - Responsive design
- **Lightbox** - Photo viewing
- **Mobile-First Design** - Responsive layouts

### Deployment & DevOps
- **Nginx** - Web server (VPS)
- **Systemd** - Service management
- **Git** - Version control
- **Render.com** - Cloud hosting
- **Supabase** - Cloud storage
- **SSL/HTTPS** - Security

### Development Tools
- **Django Admin** - Content management
- **Django Debug Toolbar** - Development debugging
- **Custom Management Commands** - Maintenance tools
- **Logging System** - Application monitoring
- **Cache Framework** - Performance optimization

## 🔒 Security Features

- ✅ **CSRF Protection** - Cross-site request forgery prevention
- ✅ **SQL Injection Protection** - Django ORM security
- ✅ **XSS Protection** - Cross-site scripting prevention
- ✅ **HTTPS Support** - SSL/TLS encryption
- ✅ **Secure Headers** - Security-focused HTTP headers
- ✅ **User Authentication** - Django auth system
- ✅ **Permission System** - Role-based access control
- ✅ **Input Validation** - Form and data validation

## 📈 Performance Features

- ✅ **Database Optimization** - Indexed queries and connection pooling
- ✅ **Static File Caching** - WhiteNoise compression
- ✅ **Template Caching** - Rendered template caching
- ✅ **Image Optimization** - Automatic image processing
- ✅ **CDN Support** - Supabase CDN integration
- ✅ **Lazy Loading** - Efficient resource loading
- ✅ **Cache Middleware** - Application-level caching
- ✅ **Database Connection Pooling** - Efficient DB connections

## 🐛 Troubleshooting

### Common Issues

**Images Not Displaying:**
```bash
# Check media directory permissions
chmod -R 755 gallery/

# Verify static files
python manage.py collectstatic
```

**Database Connection Issues:**
```bash
# Test database connection
python manage.py dbshell

# Run migrations
python manage.py migrate
```

**Service Not Starting (VPS):**
```bash
# Check service status
systemctl status kapadiaschool

# View logs
journalctl -u kapadiaschool -f
```

### Support Resources
- **Scripts**: Check `scripts/` folder for maintenance tools
- **Logs**: Check `logs/` folder for error details
- **Documentation**: Comprehensive guides in `docs/` folder
- **Django Docs**: [Official Django Documentation](https://docs.djangoproject.com/)

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🎯 Project Status: Production Ready ✅

### Completed Features:
- ✅ Multi-campus website structure
- ✅ Campus-specific photo galleries
- ✅ Mobile-responsive design
- ✅ Admin panel with role management
- ✅ VPS deployment automation
- ✅ Cloud deployment support
- ✅ Complete documentation
- ✅ Project organization and cleanup

### Ready For:
- ✅ Production deployment
- ✅ Content management by your team
- ✅ Adding campus photos
- ✅ User role management
- ✅ Ongoing maintenance

---

**Version**: 2.0 (Campus Gallery Edition)  
**Last Updated**: July 2025  
**Status**: Production Ready ✅

*Built with ❤️ for Kapadia High School*
