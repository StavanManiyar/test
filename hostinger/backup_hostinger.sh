#!/bin/bash

# Hostinger VPS Backup Script
# Automated backup system optimized for 4GB RAM, 50GB SSD

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
BACKUP_DIR="/root/backups"
DATE=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=30
WEEKLY_RETENTION=12  # Keep 12 weeks of weekly backups
MAX_BACKUP_SIZE="2G"  # Maximum backup size

echo "🔄 Starting Hostinger VPS backup process..."
echo "⏰ Backup started at: $(date)"
echo ""

# Create backup directory
mkdir -p $BACKUP_DIR

# Function to check available space
check_space() {
    local required_space=$1
    local available_space=$(df $BACKUP_DIR | awk 'NR==2 {print $4}')
    local required_kb=$((required_space * 1024 * 1024))  # Convert GB to KB
    
    if [ $available_kb -lt $required_kb ]; then
        echo -e "${RED}❌ Insufficient disk space for backup${NC}"
        echo "Required: ${required_space}GB, Available: $((available_space / 1024 / 1024))GB"
        return 1
    fi
    return 0
}

# Database Backup
echo -e "${BLUE}🗄️  Starting database backup...${NC}"
if docker ps | grep -q postgres; then
    DB_BACKUP_FILE="$BACKUP_DIR/db_backup_$DATE.sql"
    
    # Create database backup
    if docker-compose -f docker-compose.hostinger.yml exec -T db pg_dump -U postgres postgres > $DB_BACKUP_FILE; then
        DB_SIZE=$(du -h $DB_BACKUP_FILE | cut -f1)
        echo -e "${GREEN}✅ Database backup completed: $DB_SIZE${NC}"
        
        # Compress database backup
        if command -v gzip &> /dev/null; then
            gzip $DB_BACKUP_FILE
            COMPRESSED_SIZE=$(du -h ${DB_BACKUP_FILE}.gz | cut -f1)
            echo -e "${GREEN}✅ Database compressed: $COMPRESSED_SIZE${NC}"
        fi
    else
        echo -e "${RED}❌ Database backup failed${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  PostgreSQL container not running${NC}"
fi

# Media Files Backup (Weekly or if forced)
echo -e "${BLUE}📁 Checking media files backup...${NC}"
MEDIA_BACKUP_FILE="$BACKUP_DIR/media_backup_$DATE.tar.gz"
LAST_MEDIA_BACKUP=$(find $BACKUP_DIR -name "media_backup_*.tar.gz" -mtime -7 | head -1)

# Force media backup on Sundays or if no recent backup exists
if [ $(date +%u) -eq 7 ] || [ -z "$LAST_MEDIA_BACKUP" ] || [ "$1" = "--force-media" ]; then
    echo -e "${BLUE}📸 Creating media files backup...${NC}"
    
    if [ -d "gallery" ] && [ "$(ls -A gallery)" ]; then
        # Check available space before backup
        MEDIA_SIZE=$(du -s gallery | awk '{print $1}')
        MEDIA_SIZE_GB=$((MEDIA_SIZE / 1024 / 1024))
        
        if check_space $((MEDIA_SIZE_GB + 1)); then
            if tar -czf $MEDIA_BACKUP_FILE gallery/ 2>/dev/null; then
                MEDIA_BACKUP_SIZE=$(du -h $MEDIA_BACKUP_FILE | cut -f1)
                echo -e "${GREEN}✅ Media backup completed: $MEDIA_BACKUP_SIZE${NC}"
            else
                echo -e "${RED}❌ Media backup failed${NC}"
                rm -f $MEDIA_BACKUP_FILE
            fi
        else
            echo -e "${YELLOW}⚠️  Skipping media backup due to insufficient space${NC}"
        fi
    else
        echo -e "${YELLOW}⚠️  No media files found to backup${NC}"
    fi
else
    echo -e "${GREEN}✅ Recent media backup exists, skipping${NC}"
fi

# Configuration Backup
echo -e "${BLUE}⚙️  Backing up configuration files...${NC}"
CONFIG_BACKUP_FILE="$BACKUP_DIR/config_backup_$DATE.tar.gz"

# List of important config files
CONFIG_FILES=(
    ".env"
    "docker-compose.hostinger.yml"
    "nginx.hostinger.conf"
    "ssl/"
)

# Create config backup
TEMP_CONFIG_DIR="/tmp/config_backup_$DATE"
mkdir -p $TEMP_CONFIG_DIR

for file in "${CONFIG_FILES[@]}"; do
    if [ -e "$file" ]; then
        cp -r "$file" $TEMP_CONFIG_DIR/ 2>/dev/null
    fi
done

if tar -czf $CONFIG_BACKUP_FILE -C /tmp config_backup_$DATE 2>/dev/null; then
    CONFIG_SIZE=$(du -h $CONFIG_BACKUP_FILE | cut -f1)
    echo -e "${GREEN}✅ Configuration backup completed: $CONFIG_SIZE${NC}"
    rm -rf $TEMP_CONFIG_DIR
else
    echo -e "${RED}❌ Configuration backup failed${NC}"
fi

# Docker Images Backup (Monthly)
if [ $(date +%d) -eq 1 ] || [ "$1" = "--force-docker" ]; then
    echo -e "${BLUE}🐳 Creating Docker images backup...${NC}"
    DOCKER_BACKUP_FILE="$BACKUP_DIR/docker_backup_$DATE.tar"
    
    # Get list of custom images (not base images)
    CUSTOM_IMAGES=$(docker images --format "table {{.Repository}}:{{.Tag}}" | grep -E "(test-web|hostinger)" | head -5)
    
    if [ ! -z "$CUSTOM_IMAGES" ]; then
        if docker save $CUSTOM_IMAGES -o $DOCKER_BACKUP_FILE 2>/dev/null; then
            # Compress docker backup
            gzip $DOCKER_BACKUP_FILE
            DOCKER_SIZE=$(du -h ${DOCKER_BACKUP_FILE}.gz | cut -f1)
            echo -e "${GREEN}✅ Docker images backup completed: $DOCKER_SIZE${NC}"
        else
            echo -e "${YELLOW}⚠️  Docker images backup failed or skipped${NC}"
            rm -f $DOCKER_BACKUP_FILE
        fi
    else
        echo -e "${YELLOW}⚠️  No custom Docker images found${NC}"
    fi
fi

# System Information Backup
echo -e "${BLUE}ℹ️  Saving system information...${NC}"
SYSINFO_FILE="$BACKUP_DIR/sysinfo_$DATE.txt"

cat > $SYSINFO_FILE << EOF
Hostinger VPS System Information - $(date)
==========================================

Hostname: $(hostname)
Uptime: $(uptime)
Kernel: $(uname -a)
OS: $(lsb_release -a 2>/dev/null || cat /etc/os-release)

CPU Info:
$(cat /proc/cpuinfo | grep "model name" | head -1)
Cores: $(nproc)

Memory Info:
$(free -h)

Disk Usage:
$(df -h)

Docker Version:
$(docker --version 2>/dev/null || echo "Docker not installed")

Docker Compose Version:
$(docker-compose --version 2>/dev/null || echo "Docker Compose not installed")

Running Containers:
$(docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" 2>/dev/null || echo "No containers running")

Network Configuration:
$(ip addr show | grep -E "(inet|eth0|ens)" | head -10)

Environment Variables:
$(env | grep -E "(DOMAIN|ADMIN|DEBUG)" | sort)

Installed Packages:
$(dpkg -l | grep -E "(nginx|docker|postgresql)" | awk '{print $2 " " $3}')
EOF

echo -e "${GREEN}✅ System information saved${NC}"

# Cleanup Old Backups
echo -e "${BLUE}🧹 Cleaning up old backups...${NC}"

# Remove backups older than retention period
DELETED_COUNT=0

# Daily backups cleanup
find $BACKUP_DIR -name "db_backup_*.sql.gz" -mtime +$RETENTION_DAYS -type f | while read file; do
    rm "$file" && ((DELETED_COUNT++))
done

find $BACKUP_DIR -name "config_backup_*.tar.gz" -mtime +$RETENTION_DAYS -type f | while read file; do
    rm "$file" && ((DELETED_COUNT++))
done

find $BACKUP_DIR -name "sysinfo_*.txt" -mtime +$RETENTION_DAYS -type f | while read file; do
    rm "$file" && ((DELETED_COUNT++))
done

# Weekly backups cleanup (keep longer)
find $BACKUP_DIR -name "media_backup_*.tar.gz" -mtime +$((WEEKLY_RETENTION * 7)) -type f | while read file; do
    rm "$file" && ((DELETED_COUNT++))
done

# Monthly backups cleanup
find $BACKUP_DIR -name "docker_backup_*.tar.gz" -mtime +365 -type f | while read file; do
    rm "$file" && ((DELETED_COUNT++))
done

echo -e "${GREEN}✅ Cleanup completed${NC}"

# Backup Summary
echo ""
echo -e "${GREEN}📊 BACKUP SUMMARY${NC}"
echo "=================="
echo "📅 Date: $(date)"
echo "📁 Backup Directory: $BACKUP_DIR"
echo "💾 Total Backup Size: $(du -sh $BACKUP_DIR | cut -f1)"
echo "📈 Available Space: $(df -h $BACKUP_DIR | awk 'NR==2 {print $4}')"

# List recent backups
echo ""
echo "Recent Backups:"
ls -lah $BACKUP_DIR/*_$DATE.* 2>/dev/null | awk '{print "  " $9 " - " $5}' || echo "  No backups created today"

# Health Check
echo ""
echo -e "${BLUE}🏥 BACKUP HEALTH CHECK${NC}"
echo "======================"

# Check if essential backups exist
if [ -f "$BACKUP_DIR/db_backup_$DATE.sql.gz" ] || [ -f "$BACKUP_DIR/db_backup_$DATE.sql" ]; then
    echo -e "Database: ${GREEN}✅ OK${NC}"
else
    echo -e "Database: ${RED}❌ FAILED${NC}"
fi

if [ -f "$CONFIG_BACKUP_FILE" ]; then
    echo -e "Configuration: ${GREEN}✅ OK${NC}"
else
    echo -e "Configuration: ${RED}❌ FAILED${NC}"
fi

if [ -f "$SYSINFO_FILE" ]; then
    echo -e "System Info: ${GREEN}✅ OK${NC}"
else
    echo -e "System Info: ${RED}❌ FAILED${NC}"
fi

# Disk space warning
DISK_USAGE=$(df $BACKUP_DIR | awk 'NR==2 {print $5}' | sed 's/%//')
if [ $DISK_USAGE -gt 85 ]; then
    echo -e "Disk Space: ${RED}⚠️  WARNING - ${DISK_USAGE}% used${NC}"
elif [ $DISK_USAGE -gt 70 ]; then
    echo -e "Disk Space: ${YELLOW}⚠️  CAUTION - ${DISK_USAGE}% used${NC}"
else
    echo -e "Disk Space: ${GREEN}✅ OK - ${DISK_USAGE}% used${NC}"
fi

echo ""
echo -e "${GREEN}✅ Backup process completed successfully!${NC}"
echo "⏰ Backup finished at: $(date)"

# Optional: Send notification (if configured)
if command -v mail &> /dev/null && [ ! -z "$BACKUP_EMAIL" ]; then
    echo "Hostinger VPS backup completed at $(date)" | mail -s "Backup Report - $(hostname)" $BACKUP_EMAIL
fi
