#!/bin/bash

# Setup Cron Jobs for Kapadia School VPS
# This script configures automated maintenance tasks

APP_DIR="/var/www/kapadiaschool"

echo "🕐 Setting up automated maintenance tasks..."

# Create cron jobs
CRON_TEMP=$(mktemp)

# Add existing cron jobs (if any)
crontab -l 2>/dev/null >> $CRON_TEMP || echo "# Kapadia School Cron Jobs" > $CRON_TEMP

# Check if our jobs already exist
if ! grep -q "Kapadia School" $CRON_TEMP; then
    echo "" >> $CRON_TEMP
    echo "# Kapadia School Automated Maintenance" >> $CRON_TEMP
    
    # Daily backup at 2 AM
    echo "0 2 * * * $APP_DIR/backup_script.sh" >> $CRON_TEMP
    
    # Health check every 30 minutes
    echo "*/30 * * * * $APP_DIR/health_check.sh" >> $CRON_TEMP
    
    # Database optimization weekly (Sunday 3 AM)
    echo "0 3 * * 0 cd $APP_DIR && source venv/bin/activate && python manage.py optimize_db --create-indexes" >> $CRON_TEMP
    
    # SSL certificate renewal check (12th of every month at 12 PM)
    echo "0 12 12 * * /usr/bin/certbot renew --quiet" >> $CRON_TEMP
    
    # Django session cleanup daily (1 AM)
    echo "0 1 * * * cd $APP_DIR && source venv/bin/activate && python manage.py clearsessions" >> $CRON_TEMP
    
    # Log rotation weekly (Sunday 4 AM)
    echo "0 4 * * 0 /usr/sbin/logrotate /etc/logrotate.conf" >> $CRON_TEMP
fi

# Install the new cron jobs
crontab $CRON_TEMP
rm $CRON_TEMP

echo "✅ Cron jobs configured successfully!"
echo ""
echo "Scheduled tasks:"
echo "  📦 Daily backup: 2:00 AM"
echo "  🩺 Health check: Every 30 minutes"
echo "  🗂️  Database optimization: Sunday 3:00 AM"
echo "  🔒 SSL renewal check: 12th of month, 12:00 PM"
echo "  🧹 Session cleanup: Daily 1:00 AM"
echo "  📋 Log rotation: Sunday 4:00 AM"
echo ""
echo "View current cron jobs: crontab -l"
echo "Edit cron jobs: crontab -e"
