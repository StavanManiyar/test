#!/bin/bash

# Production Deployment Script for Kapadia High School Website
set -e

echo "🚀 Starting production deployment..."

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
    
    if [ ! -f "docker-compose.prod.yml" ]; then
        echo -e "${RED}❌ docker-compose.prod.yml not found!${NC}"
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
    echo -e "${BLUE}🔧 Updating nginx configuration...${NC}"
    
    # Create production nginx config with actual domain
    cp nginx.prod.conf nginx.prod.conf.tmp
    sed -i "s/DOMAIN_NAME/$DOMAIN_NAME/g" nginx.prod.conf.tmp
    
    echo -e "${GREEN}✅ Nginx configuration updated${NC}"
}

# Install Docker and Docker Compose if not installed
install_docker() {
    if ! command -v docker &> /dev/null; then
        echo -e "${YELLOW}🐳 Installing Docker...${NC}"
        curl -fsSL https://get.docker.com -o get-docker.sh
        sh get-docker.sh
        usermod -aG docker $USER
        echo -e "${GREEN}✅ Docker installed${NC}"
    else
        echo -e "${GREEN}✅ Docker already installed${NC}"
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        echo -e "${YELLOW}🐳 Installing Docker Compose...${NC}"
        curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
        chmod +x /usr/local/bin/docker-compose
        echo -e "${GREEN}✅ Docker Compose installed${NC}"
    else
        echo -e "${GREEN}✅ Docker Compose already installed${NC}"
    fi
}

# Setup SSL certificates with Let's Encrypt
setup_ssl() {
    echo -e "${BLUE}🔒 Setting up SSL certificates...${NC}"
    
    # Create SSL directory
    mkdir -p ssl
    
    # Install certbot if not installed
    if ! command -v certbot &> /dev/null; then
        apt-get update
        apt-get install -y certbot
    fi
    
    # Stop any running containers
    docker-compose -f docker-compose.prod.yml down || true
    
    # Start nginx temporarily for certificate generation
    docker run --rm -d \
        --name temp-nginx \
        -p 80:80 \
        -v "$(pwd)/ssl:/etc/nginx/ssl" \
        -v "$(pwd)/nginx.temp.conf:/etc/nginx/nginx.conf" \
        nginx:alpine
    
    # Generate SSL certificate
    certbot certonly --webroot \
        --webroot-path=ssl \
        --email admin@$DOMAIN_NAME \
        --agree-tos \
        --no-eff-email \
        -d $DOMAIN_NAME \
        -d www.$DOMAIN_NAME
    
    # Stop temporary nginx
    docker stop temp-nginx || true
    
    # Copy certificates to ssl directory
    cp /etc/letsencrypt/live/$DOMAIN_NAME/fullchain.pem ssl/
    cp /etc/letsencrypt/live/$DOMAIN_NAME/privkey.pem ssl/
    
    echo -e "${GREEN}✅ SSL certificates configured${NC}"
}

# Deploy the application
deploy() {
    echo -e "${BLUE}🚀 Deploying application...${NC}"
    
    # Pull latest images
    docker-compose -f docker-compose.prod.yml pull
    
    # Build and start services
    docker-compose -f docker-compose.prod.yml up -d --build
    
    # Wait for services to start
    echo -e "${YELLOW}⏳ Waiting for services to start...${NC}"
    sleep 30
    
    # Run migrations
    docker-compose -f docker-compose.prod.yml exec -T web python manage.py migrate
    
    # Collect static files
    docker-compose -f docker-compose.prod.yml exec -T web python manage.py collectstatic --noinput
    
    # Create superuser if needed
    echo -e "${YELLOW}👤 Creating admin user (optional)...${NC}"
    docker-compose -f docker-compose.prod.yml exec web python manage.py manage_admin_users --create-superuser || true
    
    echo -e "${GREEN}✅ Application deployed successfully!${NC}"
}

# Setup monitoring and backups
setup_monitoring() {
    echo -e "${BLUE}📊 Setting up monitoring...${NC}"
    
    # Create backup script
    cat > backup.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
docker-compose -f docker-compose.prod.yml exec -T db pg_dump -U postgres postgres > backup_$DATE.sql
find . -name "backup_*.sql" -mtime +7 -delete
EOF
    chmod +x backup.sh
    
    # Add to crontab for daily backups
    (crontab -l 2>/dev/null; echo "0 2 * * * $(pwd)/backup.sh") | crontab -
    
    echo -e "${GREEN}✅ Monitoring and backups configured${NC}"
}

# Main deployment function
main() {
    echo -e "${GREEN}"
    echo "🎓 Kapadia High School Website Deployment"
    echo "=========================================="
    echo -e "${NC}"
    
    check_files
    load_env
    update_nginx_config
    install_docker
    setup_ssl
    deploy
    setup_monitoring
    
    echo -e "${GREEN}"
    echo "🎉 Deployment completed successfully!"
    echo "======================================"
    echo -e "${NC}"
    echo -e "${BLUE}Your website is now available at:${NC}"
    echo -e "${GREEN}🌐 https://$DOMAIN_NAME${NC}"
    echo -e "${GREEN}🌐 https://www.$DOMAIN_NAME${NC}"
    echo ""
    echo -e "${BLUE}Admin panel:${NC}"
    echo -e "${GREEN}🔐 https://$DOMAIN_NAME/$ADMIN_URL${NC}"
    echo ""
    echo -e "${YELLOW}📋 Next steps:${NC}"
    echo "1. Test your website at https://$DOMAIN_NAME"
    echo "2. Login to admin panel and add content"
    echo "3. Setup regular backups"
    echo "4. Monitor server resources"
}

# Run main function
main "$@"
