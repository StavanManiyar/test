#!/bin/bash

# VPS Deployment Script for Kapadia School
# This script deploys the Django application to your VPS server

set -e  # Exit on error

echo "🚀 Starting VPS deployment process..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
VPS_USER="root"  # Change this to your VPS username
VPS_HOST="your-vps-ip"  # Change this to your VPS IP
PROJECT_DIR="/var/www/kapadiaschool"  # Change this to your desired project directory
DOMAIN="kapadiahighschool.com"  # Your domain

echo -e "${YELLOW}📋 Deployment Configuration:${NC}"
echo -e "VPS User: ${VPS_USER}"
echo -e "VPS Host: ${VPS_HOST}"
echo -e "Project Directory: ${PROJECT_DIR}"
echo -e "Domain: ${DOMAIN}"
echo ""

# Step 1: Upload project files to VPS
echo -e "${YELLOW}📁 Step 1: Uploading project files to VPS...${NC}"
rsync -avz --exclude='.git' --exclude='__pycache__' --exclude='*.pyc' --exclude='db.sqlite3' --exclude='venv' ./ ${VPS_USER}@${VPS_HOST}:${PROJECT_DIR}/

# Step 2: Install dependencies and setup on VPS
echo -e "${YELLOW}⚙️  Step 2: Setting up application on VPS...${NC}"
ssh ${VPS_USER}@${VPS_HOST} << EOF
    cd ${PROJECT_DIR}
    
    # Create virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
        echo "Creating virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Install/upgrade pip
    pip install --upgrade pip
    
    # Install dependencies
    pip install -r requirements.txt
    
    # Create necessary directories
    mkdir -p gallery/festival/images
    mkdir -p gallery/festival/gallery
    mkdir -p gallery/thumbnails
    mkdir -p gallery/images
    mkdir -p gallery/carousel/images
    mkdir -p logs
    mkdir -p staticfiles
    
    # Set permissions
    chmod -R 755 gallery/
    chmod -R 755 logs/
    chmod -R 755 staticfiles/
    
    # Collect static files
    python manage.py collectstatic --noinput
    
    # Apply database migrations
    python manage.py migrate
    
    # Create superuser for production
    echo "Creating production superuser..."
    python manage.py shell << PYTHON
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@kapadiaschool.com', 'secure_password_123')
    print('Superuser created successfully!')
else:
    print('Superuser already exists!')
PYTHON
    
    # Setup sample campus galleries (optional)
    echo "Setting up sample campus galleries..."
    python manage.py shell << PYTHON
from khschool.models import Gallery

# Create sample galleries for each campus
campus_galleries = [
    {'name': 'Chattral Campus Infrastructure', 'campus_branch': 'chattral', 'category': 'academic'},
    {'name': 'Kadi Campus Facilities', 'campus_branch': 'kadi', 'category': 'academic'},
    {'name': 'IFFCO Campus Overview', 'campus_branch': 'iffco', 'category': 'academic'},
    {'name': 'Chandkheda Campus Activities', 'campus_branch': 'chandkheda', 'category': 'event'},
]

for gallery_data in campus_galleries:
    gallery, created = Gallery.objects.get_or_create(
        name=gallery_data['name'],
        defaults={
            'campus_branch': gallery_data['campus_branch'],
            'category': gallery_data['category'],
            'description': f"Photos from {gallery_data['campus_branch'].title()} campus",
            'show_on_campus_page': True
        }
    )
    if created:
        print(f"Created gallery: {gallery.name}")
    else:
        print(f"Gallery already exists: {gallery.name}")
PYTHON
    
    # Test the application
    python manage.py check
    
    echo "✅ Application setup completed successfully!"
EOF

# Step 3: Configure Nginx (if needed)
echo -e "${YELLOW}🌐 Step 3: Configuring Nginx...${NC}"
ssh ${VPS_USER}@${VPS_HOST} << EOF
    # Create Nginx configuration
    cat > /etc/nginx/sites-available/kapadiaschool << 'NGINX_CONFIG'
server {
    listen 80;
    server_name ${DOMAIN} www.${DOMAIN};
    
    # Static files
    location /static/ {
        alias ${PROJECT_DIR}/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, no-transform";
    }
    
    # Media files
    location /gallery/ {
        alias ${PROJECT_DIR}/gallery/;
        expires 30d;
        add_header Cache-Control "public, no-transform";
    }
    
    # Django application
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
NGINX_CONFIG
    
    # Enable site
    ln -sf /etc/nginx/sites-available/kapadiaschool /etc/nginx/sites-enabled/
    
    # Test Nginx configuration
    nginx -t
    
    # Reload Nginx
    systemctl reload nginx
    
    echo "✅ Nginx configured successfully!"
EOF

# Step 4: Create systemd service for Django
echo -e "${YELLOW}🔧 Step 4: Creating Django service...${NC}"
ssh ${VPS_USER}@${VPS_HOST} << EOF
    # Create systemd service file
    cat > /etc/systemd/system/kapadiaschool.service << 'SERVICE_CONFIG'
[Unit]
Description=Kapadia School Django Application
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=${PROJECT_DIR}
Environment=PATH=${PROJECT_DIR}/venv/bin
ExecStart=${PROJECT_DIR}/venv/bin/gunicorn kapadiaschool.wsgi:application --bind 127.0.0.1:8000 --workers 3
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
SERVICE_CONFIG
    
    # Reload systemd
    systemctl daemon-reload
    
    # Enable and start service
    systemctl enable kapadiaschool
    systemctl start kapadiaschool
    
    # Check service status
    systemctl status kapadiaschool
    
    echo "✅ Django service created and started!"
EOF

echo -e "${GREEN}🎉 Deployment completed successfully!${NC}"
echo ""
echo -e "${YELLOW}📝 Next Steps:${NC}"
echo "1. Access your website at: http://${DOMAIN}"
echo "2. Access Django admin at: http://${DOMAIN}/admin"
echo "3. Login with username: admin"
echo "4. Configure SSL certificate for HTTPS"
echo ""
echo -e "${YELLOW}🛠️  Service Management Commands:${NC}"
echo "Start service: systemctl start kapadiaschool"
echo "Stop service: systemctl stop kapadiaschool"
echo "Restart service: systemctl restart kapadiaschool"
echo "View logs: journalctl -u kapadiaschool -f"
