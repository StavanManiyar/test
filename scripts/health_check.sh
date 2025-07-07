#!/bin/bash

# VPS Health Check Script for Kapadia School
# This script monitors the health of the application and services

set -e

APP_DIR="/var/www/kapadiaschool"
LOG_FILE="/var/log/kapadiaschool_health.log"
DATE=$(date '+%Y-%m-%d %H:%M:%S')

# Function to log messages
log_message() {
    echo "[$DATE] $1" | tee -a $LOG_FILE
}

# Function to check service status
check_service() {
    local service_name=$1
    if systemctl is-active --quiet $service_name; then
        log_message "✅ $service_name is running"
        return 0
    else
        log_message "❌ $service_name is not running"
        return 1
    fi
}

# Function to check supervisor programs
check_supervisor() {
    local program_name=$1
    status=$(sudo supervisorctl status $program_name | awk '{print $2}')
    if [ "$status" = "RUNNING" ]; then
        log_message "✅ $program_name is running"
        return 0
    else
        log_message "❌ $program_name is not running (status: $status)"
        return 1
    fi
}

# Function to check HTTP response
check_http() {
    local url=$1
    local expected_codes=$2
    response=$(curl -s -o /dev/null -w "%{http_code}" $url 2>/dev/null || echo "000")
    
    for code in $expected_codes; do
        if [ "$response" = "$code" ]; then
            log_message "✅ HTTP check passed for $url (HTTP $response)"
            return 0
        fi
    done
    
    log_message "❌ HTTP check failed for $url (HTTP $response)"
    return 1
}

# Function to check database connection
check_database() {
    cd $APP_DIR
    source venv/bin/activate
    
    if python manage.py shell -c "from django.db import connection; cursor = connection.cursor(); print('Database connection successful')" >/dev/null 2>&1; then
        log_message "✅ Database connection successful"
        return 0
    else
        log_message "❌ Database connection failed"
        return 1
    fi
}

# Function to check disk space
check_disk_space() {
    threshold=85
    usage=$(df /var/www | awk 'NR==2 {print $5}' | sed 's/%//')
    
    if [ $usage -lt $threshold ]; then
        log_message "✅ Disk usage is acceptable ($usage%)"
        return 0
    else
        log_message "⚠️  Warning: High disk usage ($usage%)"
        return 1
    fi
}

# Function to check memory usage
check_memory() {
    threshold=85
    usage=$(free | grep Mem | awk '{printf "%.0f", $3/$2 * 100.0}')
    
    if [ $usage -lt $threshold ]; then
        log_message "✅ Memory usage is acceptable ($usage%)"
        return 0
    else
        log_message "⚠️  Warning: High memory usage ($usage%)"
        return 1
    fi
}

# Function to check SSL certificate
check_ssl() {
    domain="kapadiahighschool.com"
    expiry_days=$(echo | openssl s_client -servername $domain -connect $domain:443 2>/dev/null | openssl x509 -noout -dates | grep notAfter | cut -d= -f2)
    
    if [ -n "$expiry_days" ]; then
        expiry_timestamp=$(date -d "$expiry_days" +%s)
        current_timestamp=$(date +%s)
        days_until_expiry=$(( (expiry_timestamp - current_timestamp) / 86400 ))
        
        if [ $days_until_expiry -gt 30 ]; then
            log_message "✅ SSL certificate valid for $days_until_expiry days"
            return 0
        else
            log_message "⚠️  Warning: SSL certificate expires in $days_until_expiry days"
            return 1
        fi
    else
        log_message "❌ Could not check SSL certificate"
        return 1
    fi
}

# Start health check
log_message "=== Starting Health Check ==="

# Initialize counters
total_checks=0
failed_checks=0

# Check system services
log_message "--- Checking System Services ---"
services=("nginx" "postgresql" "supervisor")
for service in "${services[@]}"; do
    total_checks=$((total_checks + 1))
    if ! check_service $service; then
        failed_checks=$((failed_checks + 1))
    fi
done

# Check supervisor programs
log_message "--- Checking Application Services ---"
programs=("kapadiaschool" "kapadiaschool_celery")
for program in "${programs[@]}"; do
    total_checks=$((total_checks + 1))
    if ! check_supervisor $program; then
        failed_checks=$((failed_checks + 1))
    fi
done

# Check HTTP endpoints
log_message "--- Checking HTTP Endpoints ---"
endpoints=(
    "http://localhost:8000/ 200 302"
    "https://kapadiahighschool.com/ 200"
    "https://www.kapadiahighschool.com/ 301 302"  # www should redirect
    "http://kapadiahighschool.com/ 301 302"       # http should redirect
    "http://www.kapadiahighschool.com/ 301 302"   # http www should redirect
)

for endpoint in "${endpoints[@]}"; do
    url=$(echo $endpoint | awk '{print $1}')
    codes=$(echo $endpoint | cut -d' ' -f2-)
    total_checks=$((total_checks + 1))
    if ! check_http "$url" "$codes"; then
        failed_checks=$((failed_checks + 1))
    fi
done

# Check database
log_message "--- Checking Database ---"
total_checks=$((total_checks + 1))
if ! check_database; then
    failed_checks=$((failed_checks + 1))
fi

# Check system resources
log_message "--- Checking System Resources ---"
total_checks=$((total_checks + 1))
if ! check_disk_space; then
    failed_checks=$((failed_checks + 1))
fi

total_checks=$((total_checks + 1))
if ! check_memory; then
    failed_checks=$((failed_checks + 1))
fi

# Check SSL certificate
log_message "--- Checking SSL Certificate ---"
total_checks=$((total_checks + 1))
if ! check_ssl; then
    failed_checks=$((failed_checks + 1))
fi

# Summary
log_message "=== Health Check Summary ==="
log_message "Total checks: $total_checks"
log_message "Failed checks: $failed_checks"
log_message "Success rate: $(( (total_checks - failed_checks) * 100 / total_checks ))%"

if [ $failed_checks -eq 0 ]; then
    log_message "🎉 All health checks passed!"
    exit 0
else
    log_message "⚠️  $failed_checks health check(s) failed. Please investigate."
    
# Send alert notification (uncomment and configure after setting up mail)
    if command -v mail >/dev/null 2>&1; then
        echo "Health check failed on $(hostname) at $(date). Failed checks: $failed_checks/$total_checks. Please check the logs at /var/log/kapadiaschool_health.log" | \
          mail -s "🚨 Kapadia School Health Check Alert" admin@kapadiaschool.com
        log_message "Alert email sent to admin@kapadiaschool.com"
    else
        log_message "Mail command not available. Install mailutils to enable email alerts: sudo apt install mailutils"
    fi
    
    exit 1
fi
