#!/bin/bash

# Hostinger VPS Deployment Script for Kapadia High School Website
set -e

echo "🚀 Starting Hostinger VPS deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if required files exist
check_files() {
    echo -e "${BLUE}📁 Checking required files...${NC}"
    
    if [ ! -f ".env" ]; then
        echo -e "${RED}❌ .env file not found!${NC}"
        echo -e "${YELLOW}Please copy env.production.template to .env and configure it${NC}"
        exit 1
    fi
    
    if [ ! -f "docker-compose.hostinger.yml" ]; then
        echo -e "${RED}❌ docker-compose.hostinger.yml not found!${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ All required files found${NC}"
}

# Load environment variables
load_env() {
    echo -e "${BLUE}📋 Loading environment variables...${NC}"
    source .env
    
    if [ -z "$DOMAIN_NAME" ]; then
        echo -e "${RED}❌ DOMAIN_NAME not set in .env file!${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ Environment loaded for domain: $DOMAIN_NAME${NC}"
}

# Update nginx configuration with domain name
update_nginx_config() {
    echo -e "${BLUE}🔧 Updating nginx configuration for Hostinger...${NC}"
    
    # Create Hostinger nginx config with actual domain
    cp nginx.hostinger.conf nginx.hostinger.conf.tmp
    sed -i "s/DOMAIN_NAME/$DOMAIN_NAME/g" nginx.hostinger.conf.tmp
    mv nginx.hostinger.conf.tmp nginx.hostinger.conf.ready
    
    echo -e "${GREEN}✅ Nginx configuration updated for Hostinger VPS${NC}"
}

# Install Docker and Docker Compose optimized for Hostinger
install_docker() {
    if ! command -v docker &> /dev/null; then
        echo -e "${YELLOW}🐳 Installing Docker for Hostinger VPS...${NC}"
        curl -fsSL https://get.docker.com -o get-docker.sh
        sh get-docker.sh
        usermod -aG docker $USER
        
        # Start Docker service
        systemctl enable docker
        systemctl start docker
        
        echo -e "${GREEN}✅ Docker installed and started${NC}"
    else
        echo -e "${GREEN}✅ Docker already installed${NC}"
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        echo -e "${YELLOW}🐳 Installing Docker Compose for Hostinger...${NC}"
        curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
        chmod +x /usr/local/bin/docker-compose
        echo -e "${GREEN}✅ Docker Compose installed${NC}"
    else
        echo -e "${GREEN}✅ Docker Compose already installed${NC}"
    fi
}

# Optimize system for Hostinger VPS (4GB RAM, 1 CPU)
optimize_system() {
    echo -e "${BLUE}⚡ Optimizing system for Hostinger VPS...${NC}"
    
    # Memory optimizations
    echo 'vm.swappiness=10' >> /etc/sysctl.conf
    echo 'vm.dirty_ratio=15' >> /etc/sysctl.conf
    echo 'vm.dirty_background_ratio=5' >> /etc/sysctl.conf
    echo 'vm.vfs_cache_pressure=50' >> /etc/sysctl.conf
    
    # Network optimizations
    echo 'net.core.rmem_max = 16777216' >> /etc/sysctl.conf
    echo 'net.core.wmem_max = 16777216' >> /etc/sysctl.conf
    echo 'net.ipv4.tcp_rmem = 4096 12582912 16777216' >> /etc/sysctl.conf
    echo 'net.ipv4.tcp_wmem = 4096 12582912 16777216' >> /etc/sysctl.conf
    
    # Apply settings
    sysctl -p
    
    # Create optimized PostgreSQL config
    cat > postgresql.conf << 'EOF'
# PostgreSQL configuration optimized for Hostinger VPS (4GB RAM)
shared_buffers = 1GB
effective_cache_size = 3GB
maintenance_work_mem = 256MB
checkpoint_completion_target = 0.9
wal_buffers = 16MB
default_statistics_target = 100
random_page_cost = 1.1
effective_io_concurrency = 200
work_mem = 4MB
min_wal_size = 1GB
max_wal_size = 4GB
max_worker_processes = 2
max_parallel_workers_per_gather = 1
max_parallel_workers = 2
max_parallel_maintenance_workers = 1
EOF
    
    echo -e "${GREEN}✅ System optimized for Hostinger VPS${NC}"
}

# Setup SSL certificates with Let's Encrypt
setup_ssl() {
    echo -e "${BLUE}🔒 Setting up SSL certificates for Hostinger...${NC}"
    
    # Create SSL directory
    mkdir -p ssl
    mkdir -p /var/www/certbot
    
    # Install certbot if not installed
    if ! command -v certbot &> /dev/null; then
        apt-get update
        apt-get install -y certbot
    fi
    
    # Stop any running containers
    docker-compose -f docker-compose.hostinger.yml down || true
    
    # Create temporary nginx config for certificate generation
    cat > nginx.temp.conf << 'EOF'
events {
    worker_connections 1024;
}
http {
    server {
        listen 80;
        server_name _;
        location /.well-known/acme-challenge/ {
            root /var/www/certbot;
        }
        location / {
            return 200 'OK';
            add_header Content-Type text/plain;
        }
    }
}
EOF
    
    # Start temporary nginx
    docker run --rm -d \
        --name temp-nginx \
        -p 80:80 \
        -v "$(pwd)/nginx.temp.conf:/etc/nginx/nginx.conf:ro" \
        -v "/var/www/certbot:/var/www/certbot:ro" \
        nginx:alpine
    
    sleep 5
    
    # Generate SSL certificate
    certbot certonly --webroot \
        --webroot-path=/var/www/certbot \
        --email admin@$DOMAIN_NAME \
        --agree-tos \
        --no-eff-email \
        --force-renewal \
        -d $DOMAIN_NAME \
        -d www.$DOMAIN_NAME
    
    # Stop temporary nginx
    docker stop temp-nginx || true
    
    # Copy certificates to ssl directory
    cp /etc/letsencrypt/live/$DOMAIN_NAME/fullchain.pem ssl/
    cp /etc/letsencrypt/live/$DOMAIN_NAME/privkey.pem ssl/
    
    # Set proper permissions
    chmod 644 ssl/fullchain.pem
    chmod 600 ssl/privkey.pem
    
    echo -e "${GREEN}✅ SSL certificates configured for Hostinger${NC}"
}

# Deploy the application optimized for Hostinger
deploy() {
    echo -e "${BLUE}🚀 Deploying application on Hostinger VPS...${NC}"
    
    # Use optimized nginx config
    cp nginx.hostinger.conf.ready nginx.hostinger.conf
    
    # Pull latest images
    docker-compose -f docker-compose.hostinger.yml pull
    
    # Build and start services with resource limits
    docker-compose -f docker-compose.hostinger.yml up -d --build
    
    # Wait for services to start
    echo -e "${YELLOW}⏳ Waiting for services to start (Hostinger VPS)...${NC}"
    sleep 45
    
    # Check if services are running
    if ! docker-compose -f docker-compose.hostinger.yml ps | grep -q "Up"; then
        echo -e "${RED}❌ Services failed to start. Checking logs...${NC}"
        docker-compose -f docker-compose.hostinger.yml logs
        exit 1
    fi
    
    # Run migrations
    echo -e "${BLUE}📊 Running database migrations...${NC}"
    docker-compose -f docker-compose.hostinger.yml exec -T web python manage.py migrate
    
    # Collect static files
    echo -e "${BLUE}📁 Collecting static files...${NC}"
    docker-compose -f docker-compose.hostinger.yml exec -T web python manage.py collectstatic --noinput
    
    # Create superuser if needed
    echo -e "${YELLOW}👤 Creating admin user (optional)...${NC}"
    echo "You can create an admin user later using:"
    echo "docker-compose -f docker-compose.hostinger.yml exec web python manage.py manage_admin_users --create-superuser"
    
    echo -e "${GREEN}✅ Application deployed successfully on Hostinger!${NC}"
}

# Setup monitoring and backups for Hostinger
setup_monitoring() {
    echo -e "${BLUE}📊 Setting up monitoring for Hostinger VPS...${NC}"
    
    # Install monitoring tools
    apt-get update
    apt-get install -y htop iotop ncdu
    
    # Create Hostinger-specific backup script
    cat > backup_hostinger.sh << 'EOF'
#!/bin/bash
# Hostinger VPS Backup Script
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/root/backups"
mkdir -p $BACKUP_DIR

echo "🔄 Starting Hostinger VPS backup..."

# Database backup
docker-compose -f docker-compose.hostinger.yml exec -T db pg_dump -U postgres postgres > $BACKUP_DIR/db_backup_$DATE.sql

# Compress old backups
find $BACKUP_DIR -name "*.sql" -type f -mtime +7 -exec gzip {} \;

# Remove very old backups (30+ days)
find $BACKUP_DIR -name "*.gz" -type f -mtime +30 -delete

# Media files backup (weekly)
if [ $(date +%u) -eq 1 ]; then
    tar -czf $BACKUP_DIR/media_backup_$DATE.tar.gz gallery/
fi

echo "✅ Backup completed: $BACKUP_DIR"
df -h $BACKUP_DIR
EOF
    
    chmod +x backup_hostinger.sh
    
    # Create monitoring script
    cat > monitor_hostinger.sh << 'EOF'
#!/bin/bash
echo "📊 Hostinger VPS Status Dashboard"
echo "=================================="
echo "🖥️  CPU Usage:"
top -bn1 | grep "Cpu(s)" | awk '{print $2}' | awk -F'%' '{print $1"%"}'

echo "💾 Memory Usage:"
free -h | awk 'NR==2{printf "%.1f%% (%s/%s)\n", $3*100/$2, $3, $2}'

echo "💿 Disk Usage:"
df -h / | awk 'NR==2{printf "%s (%s used)\n", $5, $3}'

echo "🐳 Docker Status:"
docker-compose -f docker-compose.hostinger.yml ps

echo "🌐 Website Health:"
curl -s -o /dev/null -w "Response Time: %{time_total}s | HTTP Code: %{http_code}\n" https://$DOMAIN_NAME || echo "❌ Website unreachable"

echo "📊 Container Resources:"
docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"
EOF
    
    chmod +x monitor_hostinger.sh
    
    # Add to crontab for daily backups
    (crontab -l 2>/dev/null; echo "0 2 * * * $(pwd)/backup_hostinger.sh") | crontab -
    
    # Setup log rotation for Hostinger
    cat > /etc/logrotate.d/docker-logs << 'EOF'
/var/lib/docker/containers/*/*.log {
  rotate 7
  daily
  compress
  size=1M
  missingok
  delaycompress
  copytruncate
}
EOF
    
    echo -e "${GREEN}✅ Monitoring and backups configured for Hostinger${NC}"
}

# Setup auto-renewal for SSL certificates
setup_ssl_renewal() {
    echo -e "${BLUE}🔄 Setting up SSL auto-renewal for Hostinger...${NC}"
    
    # Create renewal script
    cat > renew_ssl.sh << 'EOF'
#!/bin/bash
echo "🔄 Renewing SSL certificates..."

# Stop nginx temporarily
docker-compose -f docker-compose.hostinger.yml stop nginx

# Renew certificates
certbot renew --quiet

# Copy renewed certificates
if [ -f "/etc/letsencrypt/live/$DOMAIN_NAME/fullchain.pem" ]; then
    cp /etc/letsencrypt/live/$DOMAIN_NAME/fullchain.pem ssl/
    cp /etc/letsencrypt/live/$DOMAIN_NAME/privkey.pem ssl/
    chmod 644 ssl/fullchain.pem
    chmod 600 ssl/privkey.pem
fi

# Restart nginx
docker-compose -f docker-compose.hostinger.yml start nginx

echo "✅ SSL renewal completed"
EOF
    
    chmod +x renew_ssl.sh
    
    # Add to crontab for automatic renewal
    (crontab -l 2>/dev/null; echo "0 3 1 * * $(pwd)/renew_ssl.sh") | crontab -
    
    echo -e "${GREEN}✅ SSL auto-renewal configured${NC}"
}

# Main deployment function
main() {
    echo -e "${GREEN}"
    echo "🎓 Kapadia High School Website - Hostinger VPS Deployment"
    echo "=========================================================="
    echo -e "${NC}"
    
    check_files
    load_env
    update_nginx_config
    optimize_system
    install_docker
    setup_ssl
    deploy
    setup_monitoring
    setup_ssl_renewal
    
    echo -e "${GREEN}"
    echo "🎉 Hostinger VPS Deployment Completed Successfully!"
    echo "=================================================="
    echo -e "${NC}"
    echo -e "${BLUE}Your website is now live at:${NC}"
    echo -e "${GREEN}🌐 https://$DOMAIN_NAME${NC}"
    echo -e "${GREEN}🌐 https://www.$DOMAIN_NAME${NC}"
    echo ""
    echo -e "${BLUE}Admin panel:${NC}"
    echo -e "${GREEN}🔐 https://$DOMAIN_NAME/$ADMIN_URL${NC}"
    echo ""
    echo -e "${BLUE}Hostinger VPS Management:${NC}"
    echo "📊 Monitor: ./monitor_hostinger.sh"
    echo "💾 Backup: ./backup_hostinger.sh"
    echo "🔄 SSL Renew: ./renew_ssl.sh"
    echo ""
    echo -e "${YELLOW}📋 Next steps:${NC}"
    echo "1. Test your website at https://$DOMAIN_NAME"
    echo "2. Create admin user: docker-compose -f docker-compose.hostinger.yml exec web python manage.py manage_admin_users --create-superuser"
    echo "3. Login to admin panel and add content"
    echo "4. Monitor server: ./monitor_hostinger.sh"
    echo "5. Regular backups are automated daily at 2 AM"
    echo ""
    echo -e "${GREEN}🚀 Your Hostinger VPS is optimized and ready!${NC}"
}

# Run main function
main "$@"
