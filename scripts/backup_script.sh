#!/bin/bash

# VPS Backup Script for Kapadia School
# This script creates automated backups of the database and application files

set -e

# Configuration
BACKUP_DIR="/var/backups/kapadiaschool"
APP_DIR="/var/www/kapadiaschool"
DB_NAME="kapadiaschool"
DB_USER="kapadiaschool_user"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_RETENTION_DAYS=30

# Create backup directory if it doesn't exist
mkdir -p $BACKUP_DIR

echo "Starting backup process at $(date)"

# Database backup
echo "Creating database backup..."
cd $APP_DIR
source venv/bin/activate
pg_dump $DB_NAME > "$BACKUP_DIR/db_backup_$DATE.sql"
echo "Database backup completed: db_backup_$DATE.sql"

# Application files backup (excluding venv and logs)
echo "Creating application files backup..."
tar -czf "$BACKUP_DIR/app_backup_$DATE.tar.gz" \
    --exclude="venv" \
    --exclude="logs" \
    --exclude="__pycache__" \
    --exclude="*.pyc" \
    --exclude=".git" \
    -C /var/www kapadiaschool

echo "Application backup completed: app_backup_$DATE.tar.gz"

# Media files backup (gallery)
echo "Creating media files backup..."
tar -czf "$BACKUP_DIR/media_backup_$DATE.tar.gz" \
    -C $APP_DIR gallery

echo "Media backup completed: media_backup_$DATE.tar.gz"

# Cleanup old backups (older than retention days)
echo "Cleaning up old backups..."
find $BACKUP_DIR -name "*.sql" -mtime +$BACKUP_RETENTION_DAYS -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +$BACKUP_RETENTION_DAYS -delete

# Create backup summary
echo "Backup Summary - $(date)" > "$BACKUP_DIR/backup_summary_$DATE.txt"
echo "Database: db_backup_$DATE.sql" >> "$BACKUP_DIR/backup_summary_$DATE.txt"
echo "Application: app_backup_$DATE.tar.gz" >> "$BACKUP_DIR/backup_summary_$DATE.txt"
echo "Media: media_backup_$DATE.tar.gz" >> "$BACKUP_DIR/backup_summary_$DATE.txt"
echo "Total backup size:" >> "$BACKUP_DIR/backup_summary_$DATE.txt"
du -sh $BACKUP_DIR/*$DATE* >> "$BACKUP_DIR/backup_summary_$DATE.txt"

echo "Backup process completed successfully at $(date)"
echo "Backups stored in: $BACKUP_DIR"

# Send backup notification
if command -v mail >/dev/null 2>&1; then
    echo "✅ Backup completed successfully on $(hostname) at $(date). Backup files: db_backup_$DATE.sql, app_backup_$DATE.tar.gz, media_backup_$DATE.tar.gz. Total size: $(du -sh $BACKUP_DIR/*$DATE* | awk '{total+=$1} END {print total"B"}')" | \
      mail -s "✅ Kapadia School Backup Complete" admin@kapadiaschool.com
    echo "Backup notification email sent"
else
    echo "Mail command not available. Install mailutils to enable email notifications: sudo apt install mailutils"
fi
