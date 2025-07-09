# VPS Deployment Guide for Kapadia School Website

## ✅ Current Status
Your Django application is now **production-ready** with the following features:
- ✅ All URLs working correctly (200 status codes)
- ✅ PostgreSQL database integration
- ✅ Security settings configured
- ✅ Static file handling with WhiteNoise
- ✅ Image upload functionality
- ✅ Admin panel configured
- ✅ No Supabase/Render dependencies (commented out)

## 🚀 VPS Deployment Steps

### 1. Purchase and Setup Hostinger VPS
- Choose VPS plan (minimum 2GB RAM recommended)
- Select Ubuntu 20.04 or 22.04 LTS
- Note down your VPS IP address

### 2. Initial VPS Setup
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y python3 python3-pip python3-venv nginx postgresql postgresql-contrib supervisor git

# Create application user
sudo useradd -m -s /bin/bash kapadia
sudo usermod -aG sudo kapadia
```

### 3. PostgreSQL Setup
```bash
# Switch to postgres user
sudo -u postgres psql

# Create database and user
CREATE DATABASE kapadiaschool;
CREATE USER kapadia_user WITH ENCRYPTED PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE kapadiaschool TO kapadia_user;
ALTER USER kapadia_user CREATEDB;
\q
```

### 4. Application Deployment
```bash
# Switch to application user
sudo su - kapadia

# Clone your repository
git clone https://github.com/yourusername/kapadia-school.git
cd kapadia-school

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 5. Environment Configuration
Create `.env` file on VPS:
```bash
# Copy production environment template
cp .env.production .env

# Edit with your VPS details
nano .env
```

Update `.env` with:
```env
# Django Settings
SECRET_KEY=generate-a-new-secret-key-for-production
DEBUG=False

# Database Configuration
DATABASE_URL=postgres://kapadia_user:your_secure_password@localhost/kapadiaschool

# VPS Configuration
VPS_SERVER_IP=your.vps.ip.address

# Security Settings (enable after SSL setup)
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

### 6. Database Migration
```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput
```

### 7. Gunicorn Setup
```bash
# Test Gunicorn
gunicorn --bind 0.0.0.0:8000 kapadiaschool.wsgi:application

# Create Gunicorn socket file
sudo nano /etc/systemd/system/gunicorn.socket
```

Add to gunicorn.socket:
```ini
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
```

Create Gunicorn service:
```bash
sudo nano /etc/systemd/system/gunicorn.service
```

Add to gunicorn.service:
```ini
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=kapadia
Group=www-data
WorkingDirectory=/home/kapadia/kapadia-school
ExecStart=/home/kapadia/kapadia-school/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          kapadiaschool.wsgi:application

[Install]
WantedBy=multi-user.target
```

### 8. Start Services
```bash
# Start and enable Gunicorn
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket

# Check status
sudo systemctl status gunicorn.socket
```

### 9. Nginx Configuration
```bash
sudo nano /etc/nginx/sites-available/kapadiaschool
```

Add Nginx configuration:
```nginx
server {
    listen 80;
    server_name your.vps.ip.address kapadiahighschool.com www.kapadiahighschool.com;

    client_max_body_size 100M;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias /home/kapadia/kapadia-school/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    location /gallery/ {
        alias /home/kapadia/kapadia-school/gallery/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
```

### 10. Enable Site
```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/kapadiaschool /etc/nginx/sites-enabled

# Test Nginx configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx
```

### 11. SSL Setup (Optional but Recommended)
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d kapadiahighschool.com -d www.kapadiahighschool.com

# Auto-renewal
sudo systemctl status certbot.timer
```

### 12. Firewall Configuration
```bash
# Configure UFW
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

## 📋 Post-Deployment Checklist

### Test Your Website
1. Visit `http://your.vps.ip.address` 
2. Check all pages work correctly
3. Test admin panel at `/admin/`
4. Upload test images to verify media handling
5. Check that all static files load properly

### Monitor Logs
```bash
# Django logs
tail -f /home/kapadia/kapadia-school/logs/django.log

# Gunicorn logs
sudo journalctl -u gunicorn -f

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Regular Maintenance
```bash
# Update application
cd /home/kapadia/kapadia-school
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart gunicorn
```

## 🔧 Production Features Configured

### Security ✅
- HTTPS redirect (when SSL is configured)
- HSTS headers
- Secure cookies
- CSRF protection
- XSS filtering

### Performance ✅
- Static file compression (WhiteNoise)
- Database connection pooling
- Template caching
- Page caching for heavy views

### Database ✅
- PostgreSQL optimized settings
- Connection pooling
- Proper indexing

### File Handling ✅
- Local file storage (no external dependencies)
- Image optimization
- Proper media URL handling

## 🎯 Your Application is Ready!

Your Kapadia School website is now production-ready and will work perfectly on a Hostinger VPS. The application includes:
- Complete school management system
- Image galleries for different campuses
- Contact forms and information pages
- Admin interface for content management
- Responsive design
- SEO-friendly URLs

## 📞 Support
If you encounter any issues during deployment, check the logs and ensure all environment variables are properly configured in your `.env` file.
