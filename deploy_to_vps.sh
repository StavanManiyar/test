#!/bin/bash

# Quick VPS Deployment Script for Kapadia School Website
# Run this script on your VPS after basic setup

echo "🚀 Starting Kapadia School Website Deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   print_error "This script should not be run as root. Please run as a regular user with sudo privileges."
   exit 1
fi

print_status "Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

print_status "Installing Python dependencies..."
pip install -r requirements.txt

print_status "Setting up environment variables..."
if [ ! -f .env ]; then
    cp .env.production .env
    print_warning "Please edit .env file with your VPS details before continuing!"
    print_warning "nano .env"
    read -p "Press Enter after editing .env file..."
fi

print_status "Running database migrations..."
python manage.py migrate

print_status "Creating superuser..."
python manage.py createsuperuser

print_status "Collecting static files..."
python manage.py collectstatic --noinput

print_status "Creating Gunicorn socket file..."
sudo tee /etc/systemd/system/gunicorn.socket > /dev/null <<EOF
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
EOF

print_status "Creating Gunicorn service file..."
sudo tee /etc/systemd/system/gunicorn.service > /dev/null <<EOF
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=$USER
Group=www-data
WorkingDirectory=$PWD
ExecStart=$PWD/venv/bin/gunicorn \\
          --access-logfile - \\
          --workers 3 \\
          --bind unix:/run/gunicorn.sock \\
          kapadiaschool.wsgi:application

[Install]
WantedBy=multi-user.target
EOF

print_status "Starting Gunicorn services..."
sudo systemctl daemon-reload
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket

print_status "Configuring Nginx..."
sudo tee /etc/nginx/sites-available/kapadiaschool > /dev/null <<EOF
server {
    listen 80;
    server_name _;

    client_max_body_size 100M;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias $PWD/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    location /gallery/ {
        alias $PWD/gallery/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
EOF

print_status "Enabling site..."
sudo ln -sf /etc/nginx/sites-available/kapadiaschool /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

print_status "Testing Nginx configuration..."
sudo nginx -t

if [ $? -eq 0 ]; then
    print_status "Restarting Nginx..."
    sudo systemctl restart nginx
else
    print_error "Nginx configuration test failed!"
    exit 1
fi

print_status "Setting up log directory permissions..."
sudo mkdir -p logs
sudo chown -R $USER:$USER logs

print_status "Deployment completed successfully! 🎉"
echo ""
echo "🌟 Your Kapadia School website is now running!"
echo "📍 Access your site at: http://$(curl -s ifconfig.me)"
echo "🔧 Admin panel: http://$(curl -s ifconfig.me)/admin/"
echo ""
echo "📋 Next steps:"
echo "1. Update your domain DNS to point to your VPS IP"
echo "2. Configure SSL certificate with: sudo certbot --nginx"
echo "3. Update .env file with your domain name"
echo ""
echo "📊 Monitor your application:"
echo "- Django logs: tail -f logs/django.log"
echo "- Gunicorn status: sudo systemctl status gunicorn"
echo "- Nginx logs: sudo tail -f /var/log/nginx/access.log"
