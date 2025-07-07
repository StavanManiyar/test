# 🚀 Complete VPS Deployment Guide - Kapadia High School Project

This comprehensive guide covers everything from purchasing VPS hosting to deploying your Django application.

## 📋 **Prerequisites**

Before starting, ensure you have:
- ✅ Domain: `kapadiahighschool.com` (or your chosen domain)
- ✅ This project code ready (VPS-optimized, no Supabase/Render dependencies)
- ✅ Basic understanding of command line
- ✅ Credit card or payment method
- ✅ PostgreSQL knowledge (we'll install on VPS)

---

## 🛒 **PART 1: Purchase VPS Hosting on Hostinger**

### **1.1 Visit Hostinger Website**
1. Go to [https://www.hostinger.com](https://www.hostinger.com)
2. Click on **"VPS Hosting"** in the top menu
3. Or directly visit: [https://www.hostinger.com/vps-hosting](https://www.hostinger.com/vps-hosting)

### **1.2 Choose VPS Plan**
**Recommended for school website:**

| Plan | CPU | RAM | Storage | Bandwidth | Price | Recommendation |
|------|-----|-----|---------|-----------|-------|----------------|
| **KVM 1** | 1 vCPU | 4 GB | 50 GB SSD | 4 TB | ~$4.99/month | ✅ **Perfect for school** |
| **KVM 2** | 2 vCPU | 8 GB | 100 GB SSD | 8 TB | ~$8.99/month | Good for growth |
| **KVM 4** | 4 vCPU | 16 GB | 200 GB SSD | 16 TB | ~$16.99/month | Overkill for school |

**Choose KVM 1** - Perfect for your school website and cost-effective.

### **1.3 Configure Your VPS**
1. **Operating System**: Select **Ubuntu 22.04 LTS** (recommended)
2. **Data Center Location**: Choose closest to your target audience:
   - For India: Singapore or Netherlands
   - For US: US East or US West
   - For Europe: Netherlands or Lithuania
3. **Billing Period**: 
   - 48 months (cheapest per month)
   - 24 months (good balance)
   - 12 months (more flexible)

### **1.4 Complete Purchase**
1. Click **"Add to Cart"**
2. Review your order
3. Enter your personal information
4. Choose payment method
5. Complete the purchase

---

## 🔧 **PART 2: Access Your VPS**

### **2.1 Get VPS Credentials**
1. After purchase, go to [hPanel](https://hpanel.hostinger.com)
2. Login with your Hostinger account
3. Click on **"VPS"** section
4. Click on your VPS server
5. Note down:
   - **IP Address** (e.g., 123.456.789.123)
   - **Root Password** (or SSH key if you set one)

### **2.2 Connect to VPS via SSH**

**Option A: Using Windows Terminal/PowerShell**
```powershell
# Open PowerShell as Administrator
ssh root@YOUR_VPS_IP

# Enter password when prompted
```

**Option B: Using PuTTY (Windows)**
1. Download [PuTTY](https://www.putty.org/)
2. Install and open PuTTY
3. Enter your VPS IP address
4. Click "Connect"
5. Login as: `root`
6. Enter your password

**Option C: Using Hostinger's Browser Terminal**
1. In hPanel, go to your VPS
2. Click **"Browser Terminal"**
3. This opens a web-based terminal

### **2.3 Initial VPS Setup**
Once connected, run these commands:

```bash
# Update the system
apt update && apt upgrade -y

# Create a new user for security (recommended)
adduser kapadiaschool
usermod -aG sudo kapadiaschool

# Switch to new user (optional)
su - kapadiaschool
```

---

## 🌐 **PART 3: Configure Domain DNS**

### **3.1 Point Domain to VPS**

**If Domain is with Hostinger:**
1. Go to hPanel → Domains
2. Click "Manage" next to your domain
3. Go to "DNS/Nameservers" → "DNS Zone"
4. Add/Edit these records:

| Type | Name | Value | TTL |
|------|------|-------|-----|
| A | @ | YOUR_VPS_IP | 14400 |
| A | www | YOUR_VPS_IP | 14400 |

**If Domain is with Another Registrar:**
1. Login to your domain registrar (GoDaddy, Namecheap, etc.)
2. Find "DNS Management" or "DNS Settings"
3. Add the same records as above

### **3.2 Verify DNS Propagation**
DNS changes can take 24-48 hours. Check status:

**Online Tools:**
- [https://www.whatsmydns.net](https://www.whatsmydns.net)
- [https://dnschecker.org](https://dnschecker.org)

**Command Line:**
```bash
# Check if domain points to your VPS
nslookup kapadiahighschool.com
nslookup www.kapadiahighschool.com
```

---

## 📦 **PART 4: Install Required Software**

### **4.1 Install System Dependencies**
```bash
# Install Python, Nginx, PostgreSQL, and other dependencies
sudo apt install -y python3 python3-pip python3-venv nginx supervisor git
sudo apt install -y postgresql postgresql-contrib
```

### **4.2 Setup PostgreSQL Database**
```bash
# Create database and user
sudo -u postgres psql
CREATE DATABASE kapadiaschool;
CREATE USER kapadiaschool_user WITH PASSWORD 'your_strong_password_here';
GRANT ALL PRIVILEGES ON DATABASE kapadiaschool TO kapadiaschool_user;
ALTER USER kapadiaschool_user CREATEDB;
\q
```

**Important:** Remember the password you set - you'll need it later!

---

## 📥 **PART 5: Deploy Your Website**

### **5.1 Upload Your Code**

**Option A: Using Git (Recommended)**
```bash
# Install Git if not already installed
sudo apt install git -y

# Clone your repository
cd /var/www/
sudo git clone https://github.com/yourusername/kapadiaschool.git
sudo chown -R www-data:www-data kapadiaschool
cd kapadiaschool
```

**Option B: Upload via SCP/SFTP**
```bash
# From your local computer (Windows PowerShell)
scp -r C:\Users\jvs\Desktop\test root@YOUR_VPS_IP:/var/www/

# Or use FileZilla/WinSCP with these settings:
# Host: YOUR_VPS_IP
# Username: root
# Password: YOUR_VPS_PASSWORD
# Port: 22
```

### **5.2 Run Deployment Script**
```bash
# Navigate to your project
cd /var/www/kapadiaschool

# Make scripts executable
chmod +x scripts/*.sh
chmod +x deploy_vps.sh

# Run the deployment script
sudo ./deploy_vps.sh
```

This script will automatically:
- Create Python virtual environment
- Install dependencies from requirements.txt
- Setup directory structure
- Configure basic settings

### **5.3 Configure Environment Variables**
```bash
# Copy environment template
sudo cp .env.example .env

# Edit environment file
sudo nano .env
```

Add your specific values:
```env
SECRET_KEY=your-generated-secret-key-here
DEBUG=False
DATABASE_URL=postgres://kapadiaschool_user:your_password_here@localhost/kapadiaschool
VPS_SERVER_IP=YOUR_VPS_IP
ALLOWED_HOSTS=kapadiahighschool.com,www.kapadiahighschool.com,YOUR_VPS_IP
```

To generate a secret key:
```bash
cd /var/www/kapadiaschool
source venv/bin/activate
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## ⚙️ **PART 6: Configure Services**

### **6.1 Setup Nginx**
```bash
# Copy Nginx configuration
sudo cp /var/www/kapadiaschool/nginx.conf /etc/nginx/sites-available/kapadiaschool

# Enable the site
sudo ln -s /etc/nginx/sites-available/kapadiaschool /etc/nginx/sites-enabled/

# Remove default site
sudo rm -f /etc/nginx/sites-enabled/default

# Test configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx
sudo systemctl enable nginx
```

### **6.2 Setup Supervisor**
```bash
# Copy Supervisor configuration
sudo cp /var/www/kapadiaschool/supervisor.conf /etc/supervisor/conf.d/kapadiaschool.conf

# Edit the configuration to add your secret key
sudo nano /etc/supervisor/conf.d/kapadiaschool.conf
# Replace "your-secret-key-here" with your actual secret key

# Reload Supervisor
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start kapadiaschool_group:*
```

### **6.3 Setup Systemd Service (Alternative to Supervisor)**
```bash
# Copy systemd service file
sudo cp /var/www/kapadiaschool/kapadiaschool.service /etc/systemd/system/

# Enable and start the service
sudo systemctl daemon-reload
sudo systemctl enable kapadiaschool
sudo systemctl start kapadiaschool
```

### **6.4 Run Django Setup**
```bash
cd /var/www/kapadiaschool
source venv/bin/activate

# Run migrations
python manage.py migrate

# Create superuser for admin access
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput

# Test Django setup
python manage.py check --deploy
```

---

## 🔒 **PART 7: Setup SSL Certificate**

### **7.1 Install Certbot**
```bash
sudo apt install certbot python3-certbot-nginx -y
```

### **7.2 Get SSL Certificate**
```bash
# Get certificate for both domain versions
sudo certbot --nginx -d kapadiahighschool.com -d www.kapadiahighschool.com

# Follow the prompts:
# 1. Enter email address
# 2. Agree to terms
# 3. Choose whether to share email with EFF
# 4. Select option 2 (redirect HTTP to HTTPS)
```

### **7.3 Test Auto-Renewal**
```bash
# Test renewal
sudo certbot renew --dry-run

# Setup automatic renewal
sudo crontab -e
# Add this line:
0 12 * * * /usr/bin/certbot renew --quiet
```

---

## 🚀 **PART 8: Final Configuration**

### **8.1 Setup Firewall**
```bash
# Setup UFW firewall
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw --force enable

# Check status
sudo ufw status
```

### **8.2 Setup Automated Maintenance**
```bash
cd /var/www/kapadiaschool

# Setup cron jobs for maintenance
sudo chmod +x scripts/setup_cron.sh
sudo ./scripts/setup_cron.sh

# This will automatically setup:
# - Daily backups at 2 AM
# - Health checks every 30 minutes
# - Database optimization weekly
# - SSL renewal monthly
```

### **8.3 Create Media Directories**
```bash
# Create and set permissions for media files
sudo mkdir -p /var/www/kapadiaschool/media
sudo mkdir -p /var/www/kapadiaschool/media/gallery
sudo mkdir -p /var/www/kapadiaschool/media/branch_photos
sudo chown -R www-data:www-data /var/www/kapadiaschool/media
sudo chmod -R 755 /var/www/kapadiaschool/media
```

### **8.4 Restart All Services**
```bash
# Restart everything
sudo supervisorctl restart kapadiaschool_group:*
# OR if using systemd:
# sudo systemctl restart kapadiaschool

sudo systemctl restart nginx
sudo systemctl restart postgresql
```

---

## ✅ **PART 9: Test Your Website**

### **9.1 Check Website Access**
1. Open browser and visit:
   - `http://kapadiahighschool.com` (should redirect to HTTPS)
   - `https://kapadiahighschool.com` ✅
   - `https://www.kapadiahighschool.com` ✅

### **9.2 Test Admin Panel**
1. Visit: `https://kapadiahighschool.com/admin/`
2. Login with the superuser you created
3. Test uploading images and creating content

### **9.3 Run Health Check**
```bash
cd /var/www/kapadiaschool
./scripts/health_check.sh
```

---

## 🛠️ **PART 10: Monitoring & Maintenance**

### **10.1 Essential Commands**
```bash
# Check all services status
sudo supervisorctl status && sudo systemctl status nginx

# View Django logs
sudo tail -f /var/www/kapadiaschool/logs/gunicorn.log

# View Nginx logs
sudo tail -f /var/log/nginx/kapadiaschool_error.log

# Restart everything
sudo supervisorctl restart kapadiaschool_group:*
sudo systemctl restart nginx
```

### **10.2 Regular Maintenance Tasks**
```bash
# Weekly database backup
cd /var/www/kapadiaschool
./scripts/backup_script.sh

# Update application
./scripts/update_app.sh

# System updates
sudo apt update && sudo apt upgrade -y
```

### **10.3 Monitoring Website Health**
```bash
# Run health check
./scripts/health_check.sh

# Check disk space
df -h

# Check memory usage
free -m

# Check running processes
ps aux | grep python
```

---

## 🚨 **Troubleshooting Common Issues**

### **Domain Not Working:**
```bash
# Check DNS propagation
nslookup kapadiahighschool.com

# Verify Nginx configuration
sudo nginx -t

# Check if services are running
sudo supervisorctl status
sudo systemctl status nginx
```

### **SSL Certificate Issues:**
```bash
# Check certificate status
sudo certbot certificates

# Try renewing
sudo certbot renew

# Check Nginx SSL config
sudo nginx -t
```

### **Database Connection Issues:**
```bash
# Test database connection
cd /var/www/kapadiaschool
source venv/bin/activate
python manage.py shell

# In Python shell:
from django.db import connection
cursor = connection.cursor()
cursor.execute("SELECT 1")
print(cursor.fetchone())
```

### **500 Internal Server Error:**
```bash
# Check Django logs
sudo supervisorctl tail -f kapadiaschool

# Check Nginx error logs
sudo tail -f /var/log/nginx/kapadiaschool_error.log

# Check Django settings
cd /var/www/kapadiaschool
source venv/bin/activate
python manage.py check --deploy
```

### **Static Files Not Loading:**
```bash
# Recollect static files
cd /var/www/kapadiaschool
source venv/bin/activate
python manage.py collectstatic --noinput

# Check Nginx static file configuration
sudo nginx -t
sudo systemctl restart nginx
```

---

## 📞 **Getting Help**

### **Hostinger Support:**
- 24/7 Live Chat: Available in hPanel
- Knowledge Base: [https://support.hostinger.com](https://support.hostinger.com)
- Email Support: Available for all plans

### **Django/PostgreSQL Issues:**
- Django Documentation: [https://docs.djangoproject.com](https://docs.djangoproject.com)
- PostgreSQL Documentation: [https://www.postgresql.org/docs/](https://www.postgresql.org/docs/)

### **Project-Specific Files:**
- **Technical Details:** `docs/VPS_HOSTINGER_DEPLOYMENT_GUIDE.md`
- **Maintenance:** `docs/MAINTENANCE_GUIDE.md`
- **Complete Project Info:** `docs/PROJECT_INDEX_VPS.md`
- **Image Upload Guide:** `docs/IMAGE_UPLOAD_GUIDE.md`

---

## 🎉 **Congratulations!**

Your Kapadia High School website is now live on VPS hosting! 

**Your website URLs:**
- ✅ https://kapadiahighschool.com
- ✅ https://www.kapadiahighschool.com

Both URLs work with automatic HTTPS redirect for security.

**What You've Accomplished:**
- ✅ VPS hosting setup on Hostinger
- ✅ Domain configuration with SSL certificate
- ✅ PostgreSQL database setup (local on VPS)
- ✅ Django application deployed with local file storage
- ✅ Nginx web server configuration
- ✅ Automated monitoring and backups
- ✅ Security hardening with firewall

**Next Steps:**
1. Login to admin panel and add school content
2. Upload photos through the admin interface
3. Test all functionality (galleries, pages, etc.)
4. Share the website with your school community

**For ongoing maintenance:**
- Run `./scripts/health_check.sh` weekly
- Monitor logs regularly
- Keep system updated with `sudo apt update && sudo apt upgrade`
- Backup data regularly using `./scripts/backup_script.sh`

Enjoy your professional school website! 🎓✨

---

**Last Updated:** 2025-01-07  
**Status:** Production Ready for VPS Deployment  
**Storage:** Local file storage (VPS-optimized)
