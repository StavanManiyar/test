# 🚀 Complete VPS Setup Guide for Kapadia High School

This guide will walk you through purchasing VPS hosting on Hostinger and deploying your website step-by-step.

## 📋 **Prerequisites**

Before starting, make sure you have:
- ✅ Domain: `kapadiahighschool.com` (already purchased)
- ✅ This project code ready
- ✅ Basic understanding of command line
- ✅ Credit card or payment method

## 🛒 **Step 1: Purchase VPS Hosting on Hostinger**

### **1.1 Visit Hostinger Website**
1. Go to [https://www.hostinger.com](https://www.hostinger.com)
2. Click on **"VPS Hosting"** in the top menu
3. Or directly visit: [https://www.hostinger.com/vps-hosting](https://www.hostinger.com/vps-hosting)

### **1.2 Choose VPS Plan**
**For a school website, I recommend:**

| Plan | CPU | RAM | Storage | Bandwidth | Price | Recommendation |
|------|-----|-----|---------|-----------|-------|----------------|
| **KVM 1** | 1 vCPU | 4 GB | 50 GB SSD | 4 TB | ~$4.99/month | ✅ **Perfect for school** |
| **KVM 2** | 2 vCPU | 8 GB | 100 GB SSD | 8 TB | ~$8.99/month | Good for growth |
| **KVM 4** | 4 vCPU | 16 GB | 200 GB SSD | 16 TB | ~$16.99/month | Overkill for school |

**Choose KVM 1** - It's perfect for your school website and very cost-effective.

### **1.3 Configure Your VPS**
1. **Operating System**: Select **Ubuntu 22.04 LTS** (recommended)
2. **Data Center Location**: Choose closest to your location:
   - For India: Singapore or Netherlands
   - For US: US East or US West
   - For Europe: Netherlands or Lithuania
3. **Billing Period**: 
   - 48 months (cheapest per month)
   - 24 months (good balance)
   - 12 months (more flexible)

### **1.4 Add Domain (Optional)**
- If you bought your domain elsewhere, skip this
- If you want to buy domain through Hostinger, add it here

### **1.5 Complete Purchase**
1. Click **"Add to Cart"**
2. Review your order
3. Enter your personal information
4. Choose payment method
5. Complete the purchase

## 🔧 **Step 2: Access Your VPS**

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

# Create a new user for security (optional but recommended)
adduser kapadiaschool
usermod -aG sudo kapadiaschool

# Switch to new user (optional)
su - kapadiaschool
```

## 🌐 **Step 3: Configure Domain DNS**

### **3.1 Point Domain to VPS**
You need to configure DNS to point both `kapadiahighschool.com` and `www.kapadiahighschool.com` to your VPS.

**If Domain is with Hostinger:**
1. Go to hPanel → Domains
2. Click "Manage" next to your domain
3. Go to "DNS/Nameservers" → "DNS Zone"
4. Add/Edit these records:

| Type | Name | Value | TTL |
|------|------|-------|-----|
| A | @ | YOUR_VPS_IP | 14400 |
| A | www | YOUR_VPS_IP | 14400 |
| CNAME | www | kapadiahighschool.com | 14400 |

**If Domain is with Another Registrar:**
1. Login to your domain registrar (GoDaddy, Namecheap, etc.)
2. Find "DNS Management" or "DNS Settings"
3. Add the same records as above

### **3.2 Verify DNS Propagation**
DNS changes can take 24-48 hours to propagate. Check status:

**Online Tools:**
- [https://www.whatsmydns.net](https://www.whatsmydns.net)
- [https://dnschecker.org](https://dnschecker.org)

**Command Line:**
```bash
# Check if domain points to your VPS
nslookup kapadiahighschool.com
nslookup www.kapadiahighschool.com

# Should return your VPS IP address
```

## 📦 **Step 4: Deploy Your Website**

### **4.1 Upload Your Code**
There are several ways to get your code to the VPS:

**Option A: Using Git (Recommended)**
```bash
# Install Git
sudo apt install git -y

# Clone your repository
cd /var/www/
sudo git clone https://github.com/yourusername/kapadiaschool.git
sudo chown -R www-data:www-data kapadiaschool
```

**Option B: Upload via SCP/SFTP**
```bash
# From your local computer (Windows)
scp -r C:\Users\jvs\Desktop\kapadiaschool root@YOUR_VPS_IP:/var/www/

# Or use FileZilla/WinSCP with these settings:
# Host: YOUR_VPS_IP
# Username: root
# Password: YOUR_VPS_PASSWORD
# Port: 22
```

### **4.2 Run Deployment Script**
```bash
# Navigate to your project
cd /var/www/kapadiaschool

# Make scripts executable
chmod +x *.sh

# Run the deployment script
sudo ./deploy_vps.sh
```

### **4.3 Configure Environment Variables**
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
DATABASE_URL=postgres://kapadiaschool_user:your_password@localhost/kapadiaschool
VPS_SERVER_IP=YOUR_VPS_IP
```

To generate a secret key:
```bash
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## ⚙️ **Step 5: Configure Services**

### **5.1 Setup Nginx**
```bash
# Copy Nginx configuration
sudo cp /var/www/kapadiaschool/nginx.conf /etc/nginx/sites-available/kapadiaschool

# Enable the site
sudo ln -s /etc/nginx/sites-available/kapadiaschool /etc/nginx/sites-enabled/

# Remove default site
sudo rm /etc/nginx/sites-enabled/default

# Test configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx
sudo systemctl enable nginx
```

### **5.2 Setup Supervisor**
```bash
# Copy Supervisor configuration
sudo cp /var/www/kapadiaschool/supervisor.conf /etc/supervisor/conf.d/kapadiaschool.conf

# Update the SECRET_KEY in supervisor config
sudo nano /etc/supervisor/conf.d/kapadiaschool.conf
# Replace "your-secret-key-here" with your actual secret key

# Reload Supervisor
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start kapadiaschool_group:*
```

### **5.3 Setup Database**
```bash
# Create PostgreSQL database
sudo -u postgres psql
CREATE DATABASE kapadiaschool;
CREATE USER kapadiaschool_user WITH PASSWORD 'your_strong_password';
GRANT ALL PRIVILEGES ON DATABASE kapadiaschool TO kapadiaschool_user;
\q

# Update .env file with database credentials
sudo nano /var/www/kapadiaschool/.env
# Update DATABASE_URL with your password
```

### **5.4 Run Django Setup**
```bash
cd /var/www/kapadiaschool
source venv/bin/activate

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput

# Test setup
python manage.py setup_vps --collect-static
```

## 🔒 **Step 6: Setup SSL Certificate**

### **6.1 Install Certbot**
```bash
sudo apt install certbot python3-certbot-nginx -y
```

### **6.2 Get SSL Certificate**
```bash
# Get certificate for both domain versions
sudo certbot --nginx -d kapadiahighschool.com -d www.kapadiahighschool.com

# Follow the prompts:
# 1. Enter email address
# 2. Agree to terms
# 3. Choose whether to share email with EFF
# 4. Select option 2 (redirect HTTP to HTTPS)
```

### **6.3 Test Auto-Renewal**
```bash
# Test renewal
sudo certbot renew --dry-run

# Setup automatic renewal
sudo crontab -e
# Add this line:
0 12 * * * /usr/bin/certbot renew --quiet
```

## 🚀 **Step 7: Final Configuration**

### **7.1 Setup Automated Maintenance**
```bash
cd /var/www/kapadiaschool

# Setup cron jobs for maintenance
sudo ./setup_cron.sh

# This will automatically:
# - Backup daily at 2 AM
# - Health check every 30 minutes
# - Database optimization weekly
# - SSL renewal monthly
```

### **7.2 Configure Firewall**
```bash
# Setup UFW firewall
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw enable

# Check status
sudo ufw status
```

### **7.3 Restart All Services**
```bash
# Restart everything
sudo supervisorctl restart kapadiaschool_group:*
sudo systemctl restart nginx
sudo systemctl restart postgresql
```

## ✅ **Step 8: Test Your Website**

### **8.1 Check Website Access**
1. Open browser and visit:
   - `http://kapadiahighschool.com` (should redirect to HTTPS)
   - `https://kapadiahighschool.com` ✅
   - `https://www.kapadiahighschool.com` ✅
   - `http://www.kapadiahighschool.com` (should redirect to HTTPS)

### **8.2 Test Admin Panel**
1. Visit: `https://kapadiahighschool.com/admin/`
2. Login with the superuser you created
3. Test uploading images and creating content

### **8.3 Run Health Check**
```bash
cd /var/www/kapadiaschool
./health_check.sh
```

## 🎯 **Step 9: Post-Deployment**

### **9.1 Update Domain References**
Make sure all internal links use your new domain:
1. Update any hardcoded URLs in your code
2. Update social media links
3. Update Google Analytics/Search Console

### **9.2 Setup Monitoring**
1. Add your domain to [Google Search Console](https://search.google.com/search-console)
2. Setup [Google Analytics](https://analytics.google.com)
3. Consider uptime monitoring services like [UptimeRobot](https://uptimerobot.com)

### **9.3 Create Documentation**
```bash
# Create a quick reference file
echo "VPS IP: YOUR_VPS_IP" > /var/www/kapadiaschool/server_info.txt
echo "Domain: kapadiahighschool.com" >> /var/www/kapadiaschool/server_info.txt
echo "Admin URL: https://kapadiahighschool.com/admin/" >> /var/www/kapadiaschool/server_info.txt
echo "Deployed: $(date)" >> /var/www/kapadiaschool/server_info.txt
```

## 🛠️ **Troubleshooting Common Issues**

### **Domain Not Working:**
1. Check DNS propagation: `nslookup kapadiahighschool.com`
2. Verify Nginx configuration: `sudo nginx -t`
3. Check if services are running: `sudo supervisorctl status`

### **SSL Certificate Issues:**
1. Check certificate status: `sudo certbot certificates`
2. Try renewing: `sudo certbot renew`
3. Check Nginx SSL config: `sudo nginx -t`

### **Website Shows Nginx Default Page:**
1. Check if your site is enabled: `ls -la /etc/nginx/sites-enabled/`
2. Restart Nginx: `sudo systemctl restart nginx`
3. Check Nginx error logs: `sudo tail -f /var/log/nginx/error.log`

### **500 Internal Server Error:**
1. Check Django logs: `sudo supervisorctl tail -f kapadiaschool`
2. Check Nginx error logs: `sudo tail -f /var/log/nginx/kapadiaschool_error.log`
3. Verify database connection: `python manage.py shell`

## 📞 **Getting Help**

### **Hostinger Support:**
- 24/7 Live Chat: Available in hPanel
- Knowledge Base: [https://support.hostinger.com](https://support.hostinger.com)
- Email Support: Available for all plans

### **Useful Commands:**
```bash
# Check all services status
sudo supervisorctl status && sudo systemctl status nginx

# View logs
sudo tail -f /var/www/kapadiaschool/logs/django.log

# Restart everything
sudo supervisorctl restart kapadiaschool_group:* && sudo systemctl restart nginx
```

## 🎉 **Congratulations!**

Your Kapadia High School website is now live on VPS hosting! 

**Your website URLs:**
- ✅ https://kapadiahighschool.com
- ✅ https://www.kapadiahighschool.com

Both URLs will work and redirect to HTTPS automatically for security.

**Next Steps:**
1. Add content through the admin panel
2. Upload school photos and documents
3. Share the website with your school community
4. Monitor performance using the health check script

**For ongoing maintenance, refer to:**
- `MAINTENANCE_GUIDE.md` - Detailed maintenance procedures
- `README.md` - Complete project documentation
- `VPS_HOSTINGER_DEPLOYMENT_GUIDE.md` - Technical deployment details

Enjoy your new professional school website! 🎓✨
