# 🚀 Kapadia High School Website - Production Deployment Guide

This guide will help you deploy your Django website to a live domain using Docker.

## 📋 Prerequisites

1. **Domain Name**: You already have this! 
2. **VPS Server**: DigitalOcean, Linode, Vultr, AWS EC2, etc.
3. **Basic Terminal Knowledge**: Copy/paste commands

## 🛠️ Deployment Options

### Option 1: VPS Deployment (Recommended - $5-10/month)

#### Step 1: Get a VPS Server
**Recommended Providers:**
- **DigitalOcean**: $5/month (1GB RAM, 25GB SSD)
- **Linode**: $5/month (1GB RAM, 25GB SSD)
- **Vultr**: $3.50/month (512MB RAM, 10GB SSD)

**Choose:** Ubuntu 22.04 LTS

#### Step 2: Point Your Domain to Server
In your domain registrar (GoDaddy, Namecheap, etc.):
```
A Record: yourdomain.com → YOUR_SERVER_IP
A Record: www.yourdomain.com → YOUR_SERVER_IP
```

#### Step 3: Upload Your Project to Server
```bash
# Option A: Upload via SCP
scp -r /path/to/your/project root@YOUR_SERVER_IP:/var/www/

# Option B: Clone from GitHub (if you have repository)
git clone https://github.com/yourusername/your-repo.git /var/www/school-website
```

#### Step 4: Configure for Production
```bash
# Connect to your server
ssh root@YOUR_SERVER_IP

# Navigate to your project
cd /var/www/school-website

# Copy environment template
cp env.production.template .env

# Edit environment file
nano .env
```

**Update .env file:**
```bash
DOMAIN_NAME=yourdomain.com
SECRET_KEY=your-super-secret-key-here-change-this
DB_PASSWORD=your-secure-database-password
ADMIN_URL=your-secret-admin-path/
```

#### Step 5: Deploy
```bash
# Make deployment script executable
chmod +x deploy.sh

# Run deployment
./deploy.sh
```

This script will:
- ✅ Install Docker and Docker Compose
- ✅ Setup SSL certificates (HTTPS)
- ✅ Configure nginx with security headers
- ✅ Deploy your application
- ✅ Setup automatic backups

#### Step 6: Access Your Website
- **Website**: https://yourdomain.com
- **Admin Panel**: https://yourdomain.com/your-secret-admin-path/

---

### Option 2: DigitalOcean App Platform (Easier - $5-12/month)

#### Step 1: Prepare for App Platform
```bash
# Create app.yaml
cat > app.yaml << 'EOF'
name: kapadia-school
services:
- name: web
  source_dir: /
  github:
    repo: yourusername/your-repo
    branch: main
  run_command: gunicorn --worker-tmp-dir /dev/shm kapadiaschool.wsgi
  environment_slug: python
  instance_count: 1
  instance_size_slug: basic-xxs
  envs:
  - key: DEBUG
    value: "False"
  - key: SECRET_KEY
    value: "your-secret-key"
  - key: ADMIN_URL
    value: "admin/"
databases:
- name: db
  engine: PG
  version: "12"
EOF
```

#### Step 2: Deploy to App Platform
1. Login to DigitalOcean
2. Create new App
3. Connect your GitHub repository
4. Configure environment variables
5. Deploy!

---

### Option 3: Manual Commands (If deployment script doesn't work)

#### Server Setup:
```bash
# Update system
apt update && apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose
curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-linux-x86_64" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Install Certbot for SSL
apt install certbot -y
```

#### Deploy Application:
```bash
# Navigate to project directory
cd /var/www/school-website

# Update nginx config with your domain
sed -i 's/DOMAIN_NAME/yourdomain.com/g' nginx.prod.conf

# Get SSL certificate
certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com

# Copy SSL certificates
mkdir -p ssl
cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem ssl/
cp /etc/letsencrypt/live/yourdomain.com/privkey.pem ssl/

# Deploy with Docker Compose
docker-compose -f docker-compose.prod.yml up -d --build

# Run migrations
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate

# Collect static files
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput

# Create admin user
docker-compose -f docker-compose.prod.yml exec web python manage.py manage_admin_users --create-superuser
```

---

## 🔐 Security Configuration

### Admin Security
```bash
# Change admin URL to something secure
ADMIN_URL=super-secret-admin-panel-xyz123/

# Use strong passwords
SECRET_KEY=generate-a-64-character-random-string-here
DB_PASSWORD=use-a-strong-database-password
```

### SSL/HTTPS
The deployment script automatically:
- ✅ Gets free SSL certificates from Let's Encrypt
- ✅ Redirects HTTP to HTTPS
- ✅ Enables security headers
- ✅ Sets up automatic certificate renewal

---

## 📊 Monitoring & Maintenance

### Check Application Status
```bash
# Check running containers
docker-compose -f docker-compose.prod.yml ps

# View logs
docker-compose -f docker-compose.prod.yml logs -f web

# Check nginx logs
docker-compose -f docker-compose.prod.yml logs nginx
```

### Database Backups
```bash
# Manual backup
docker-compose -f docker-compose.prod.yml exec db pg_dump -U postgres postgres > backup.sql

# Automatic daily backups are setup by deployment script
```

### Update Application
```bash
# Pull latest code
git pull origin main

# Rebuild and restart
docker-compose -f docker-compose.prod.yml up -d --build

# Run any new migrations
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
```

---

## 🆘 Troubleshooting

### Common Issues:

#### 1. Domain not pointing to server
```bash
# Check DNS propagation
nslookup yourdomain.com
```

#### 2. SSL certificate issues
```bash
# Renew certificates
certbot renew

# Copy new certificates
cp /etc/letsencrypt/live/yourdomain.com/*.pem ssl/
docker-compose -f docker-compose.prod.yml restart nginx
```

#### 3. Application not starting
```bash
# Check logs
docker-compose -f docker-compose.prod.yml logs web

# Common fix: restart containers
docker-compose -f docker-compose.prod.yml restart
```

#### 4. Database connection issues
```bash
# Check database container
docker-compose -f docker-compose.prod.yml logs db

# Reset database password in .env file and restart
```

---

## 💰 Cost Breakdown

### VPS Option:
- **Server**: $5-10/month (DigitalOcean/Linode)
- **Domain**: $10-15/year (if not already owned)
- **SSL**: Free (Let's Encrypt)
- **Total**: ~$60-120/year

### App Platform Option:
- **Hosting**: $5-12/month
- **Database**: $15/month
- **Domain**: $10-15/year
- **Total**: ~$240-360/year

---

## 🎯 Quick Start Commands

**For VPS deployment:**
```bash
# 1. Upload your project to server
scp -r C:\Users\jvs\Desktop\test root@YOUR_SERVER_IP:/var/www/school-website

# 2. SSH to server
ssh root@YOUR_SERVER_IP

# 3. Configure and deploy
cd /var/www/school-website
cp env.production.template .env
nano .env  # Edit with your domain and secrets
chmod +x deploy.sh
./deploy.sh
```

**That's it!** Your website will be live at https://yourdomain.com

---

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review server logs: `docker-compose logs`
3. Ensure DNS is properly configured
4. Verify SSL certificates are valid

**Your website should be live within 30 minutes of running the deployment script!**
