# 🚀 Kapadia School Django Deployment Guide

## 📋 **Your Django Admin Models Overview**

When you access `/admin` with your credentials, you'll see these models:

### 🎉 **Celebrations**
- **Main Model**: Store festival/event information
- **Fields**: Name, Description, Type, Main Image, Date, Featured status
- **Related Photos**: Additional photos for each celebration
- **Admin Features**: Image previews, photo count, inline editing

### 🖼️ **Gallery**
- **Gallery Categories**: Organize images by type (festival, academic, sports, etc.)
- **Gallery Images**: Individual images within each gallery
- **Admin Features**: Thumbnail previews, image count, bulk management

### 🎠 **Carousel Images**
- **Homepage Slider**: Main banner images with call-to-action buttons
- **Admin Features**: Order management, preview, link configuration

## 💾 **Image Storage System**

### **How Images Are Stored:**
1. **Local Development**: Images stored in `gallery/` folder
2. **Production VPS**: Images stored in VPS `gallery/` folder 
3. **Database**: Stores image paths and URLs, NOT the actual images
4. **Supabase** (Optional): Cloud storage with URL references

### **Database vs File Storage:**
- ✅ **Database stores**: File paths, captions, metadata
- ✅ **File system stores**: Actual image files
- ✅ **URLs work**: Because Django serves media files via MEDIA_URL

## 🔐 **Superuser Management**

### **Local Development:**
```bash
python manage.py createsuperuser
# Creates user in LOCAL SQLite database
```

### **Production (VPS):**
```bash
# On your VPS
python manage.py createsuperuser
# Creates user in PRODUCTION PostgreSQL database
```

### **Important:** Local and production databases are separate!

## 🌐 **Deployment Options**

## **Option 1: Deploy to Render (Easy)**

### **Steps:**
1. **Push to GitHub**: Commit all your changes
2. **Connect Render**: Link your GitHub repo to Render
3. **Auto-Deploy**: Render will use `render.yaml` and `build.sh`
4. **Create Superuser**: Use Render's shell to create admin user

### **Render Deployment:**
```bash
# After deployment, access Render shell and run:
python manage.py createsuperuser
```

### **How Render Works:**
- ✅ **Automatic**: Builds from your GitHub repo
- ✅ **Database**: Managed PostgreSQL included
- ✅ **Static Files**: Automatically handled
- ✅ **SSL**: Free HTTPS certificate
- ✅ **Domain**: Custom domain support

---

## **Option 2: Deploy to Your VPS (Advanced)**

### **Prerequisites:**
1. Ubuntu/Debian VPS with root access
2. Domain pointing to your VPS IP
3. SSH access to your server

### **Deployment Steps:**

#### **1. Prepare Deployment Script:**
```bash
# Edit deploy.sh - Update these values:
VPS_USER="root"                    # Your VPS username
VPS_HOST="your-vps-ip"            # Your VPS IP address
DOMAIN="kapadiahighschool.com"    # Your domain
```

#### **2. Run Deployment:**
```bash
# Make script executable
chmod +x deploy.sh

# Run deployment (from your local machine)
./scripts/deploy.sh
```

#### **3. Manual VPS Setup (Alternative):**
```bash
# SSH into your VPS
ssh root@your-vps-ip

# Clone your project
git clone https://github.com/yourusername/kapadiaschool.git
cd kapadiaschool

# Run the build script
chmod +x build.sh
./build.sh

# Start the application
gunicorn kapadiaschool.wsgi:application --bind 0.0.0.0:8000
```

## 🔧 **Post-Deployment Tasks**

### **1. Access Your Admin Panel:**
- **URL**: `https://yoursite.com/admin`
- **Username**: `admin`
- **Password**: The one you set during superuser creation

### **2. Upload Your First Images:**
1. Go to **Celebrations** → **Add Celebration**
2. Fill in the details
3. Upload main image
4. Add additional photos using the inline forms
5. Save and view on your website!

### **3. Configure Gallery:**
1. Go to **Galleries** → **Add Gallery**
2. Set category and upload thumbnail
3. Add multiple images to the gallery
4. They'll appear automatically on your gallery page

## 🔄 **Making Updates After Deployment**

### **For Render:**
1. **Make changes locally**
2. **Commit to GitHub**: `git add . && git commit -m "Update" && git push`
3. **Auto-deploys**: Render automatically rebuilds and deploys

### **For VPS:**
```bash
# On your VPS
cd /var/www/kapadiaschool
git pull origin main
source venv/bin/activate
python manage.py collectstatic --noinput
python manage.py migrate
systemctl restart kapadiaschool
```

## 🐛 **Troubleshooting**

### **Images Not Showing:**
```bash
# Check media directory permissions
chmod -R 755 gallery/

# Verify Nginx configuration
nginx -t
systemctl reload nginx
```

### **Database Connection Issues:**
```bash
# Check database connection
python manage.py dbshell

# Run migrations if needed
python manage.py migrate
```

### **Service Not Starting:**
```bash
# Check service status
systemctl status kapadiaschool

# View logs
journalctl -u kapadiaschool -f
```

## 📞 **Need Help?**

### **Common Commands:**
```bash
# Check Django status
python manage.py check

# Create migrations
python manage.py makemigrations

# Apply migrations  
python manage.py migrate

# Collect static files
python manage.py collectstatic

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

### **Service Management (VPS):**
```bash
# Start service
systemctl start kapadiaschool

# Stop service
systemctl stop kapadiaschool

# Restart service
systemctl restart kapadiaschool

# Enable auto-start
systemctl enable kapadiaschool
```

## 🎯 **Summary**

✅ **Admin Access**: `/admin` with your superuser credentials
✅ **Image Upload**: Through admin panel, stored in gallery/ folder
✅ **Database**: Stores metadata, not actual files
✅ **Deployment**: Choose Render (easy) or VPS (advanced)
✅ **Updates**: Git push for Render, git pull + restart for VPS

Your Django application is ready for production! 🚀
