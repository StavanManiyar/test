#!/bin/bash

# VPS Build Script for Kapadia School
# This script prepares the Django application for VPS deployment

set -e  # Exit on error

echo "Starting VPS build process..."

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create media directories
echo "Creating media directories..."
mkdir -p gallery/festival/images
mkdir -p gallery/festival/gallery
mkdir -p gallery/thumbnails
mkdir -p gallery/images
mkdir -p gallery/carousel/images
mkdir -p logs

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Make migrations
echo "Making migrations..."
python manage.py makemigrations

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Create superuser if not exists
echo "Creating superuser..."
echo "from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@kapadiaschool.com', 'admin@123')" | python manage.py shell

# Test Supabase connection if configured
echo "Testing Supabase connection..."
if [ -n "$SUPABASE_URL" ] && [ -n "$SUPABASE_KEY" ]; then
  echo "Supabase credentials found, testing connection..."
  python -c "from khschool.supabase_init import supabase_client; print('Supabase connection successful')"
else
  echo "Supabase credentials not found. Using local file storage."
fi

# Test Django application
echo "Testing Django application..."
python manage.py check

echo "VPS build process completed successfully!"
