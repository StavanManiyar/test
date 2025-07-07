#!/bin/bash

# VPS Deployment Script for Hostinger
# This script sets up the Django application on a VPS server

set -e  # Exit on error

echo "Starting VPS deployment for Kapadia School..."

# Update system packages
echo "Updating system packages..."
sudo apt update
sudo apt upgrade -y

# Install Python and pip if not installed
echo "Installing Python and required packages..."
sudo apt install -y python3 python3-pip python3-venv nginx supervisor

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
echo "Creating directories..."
mkdir -p gallery/festival/images
mkdir -p gallery/festival/gallery
mkdir -p gallery/thumbnails
mkdir -p gallery/images
mkdir -p gallery/carousel/images
mkdir -p logs

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Run migrations
echo "Running database migrations..."
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional - comment out in production)
echo "Creating superuser..."
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@kapadiaschool.com', 'admin@123')" | python manage.py shell

# Test the application
echo "Testing Django application..."
python manage.py check

echo "VPS deployment completed successfully!"
echo "Next steps:"
echo "1. Configure Nginx (see nginx.conf)"
echo "2. Configure Supervisor (see supervisor.conf)"
echo "3. Set up SSL certificate"
echo "4. Configure domain DNS"
