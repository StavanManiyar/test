#!/bin/bash

# VPS Update Script for Kapadia School
# This script safely updates the application with minimal downtime

set -e

APP_DIR="/var/www/kapadiaschool"
BACKUP_DIR="/var/backups/kapadiaschool"
DATE=$(date +%Y%m%d_%H%M%S)

echo "Starting application update at $(date)"

# Change to app directory
cd $APP_DIR

# Create quick backup before update
echo "Creating pre-update backup..."
mkdir -p $BACKUP_DIR
pg_dump kapadiaschool > "$BACKUP_DIR/pre_update_backup_$DATE.sql"

# Stop application services
echo "Stopping application services..."
sudo supervisorctl stop kapadiaschool_group:*

# Pull latest changes from git
echo "Pulling latest changes from repository..."
git pull origin main

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Update dependencies
echo "Updating Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Run database migrations
echo "Running database migrations..."
python manage.py makemigrations
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Run Django checks
echo "Running Django system checks..."
python manage.py check

# Test database connection
echo "Testing database connection..."
python manage.py shell -c "from django.db import connection; cursor = connection.cursor(); print('Database connection successful')"

# Restart application services
echo "Starting application services..."
sudo supervisorctl start kapadiaschool_group:*

# Wait a moment for services to start
sleep 5

# Check if services are running
echo "Checking service status..."
sudo supervisorctl status kapadiaschool_group:*

# Test application is responding
echo "Testing application response..."
response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/ || echo "000")
if [ "$response" = "200" ] || [ "$response" = "302" ]; then
    echo "✅ Application is responding correctly (HTTP $response)"
else
    echo "❌ Application may not be responding correctly (HTTP $response)"
    echo "Check logs: sudo supervisorctl tail -f kapadiaschool"
fi

# Reload Nginx configuration
echo "Reloading Nginx configuration..."
sudo nginx -t && sudo systemctl reload nginx

echo "Application update completed successfully at $(date)"
echo "Pre-update backup saved as: pre_update_backup_$DATE.sql"

# Optional: Send update notification
# echo "Application update completed successfully on $(hostname) at $(date)" | mail -s "Kapadia School App Updated" admin@kapadiaschool.com
