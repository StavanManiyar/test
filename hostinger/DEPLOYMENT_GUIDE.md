# 🚀 Hostinger VPS Deployment Guide - Kapadia High School Website

Complete step-by-step guide to deploy your Django website on Hostinger VPS.

## 📋 What You'll Need

1. ✅ **Hostinger VPS KVM1** (₹5,998/year)
2. ✅ **Your Domain** (already purchased)
3. ✅ **This Project Folder** (C:\Users\jvs\Desktop\test)
4. ✅ **15-30 minutes** of your time

---

## 🛒 **Step 1: Purchase Hostinger VPS**

### **Buy VPS:**
1. Go to **Hostinger.com**
2. Select **VPS Hosting**
3. Choose **KVM 1** plan (₹5,998/year)
4. Complete purchase

### **Setup VPS:**
1. Login to **Hostinger Panel**
2. Go to **VPS** section
3. Click **Manage** on your VPS
4. Choose **Operating System**: **Ubuntu 22.04 LTS**
5. Set **Root Password** (save this!)
6. Wait 5-10 minutes for setup

### **Get Your VPS Details:**
```
VPS IP Address: XXX.XXX.XXX.XXX (note this down)
Username: root
Password: (your chosen password)
```

---

## 🌐 **Step 2: Configure Your Domain**

### **Point Domain to Hostinger VPS:**
1. Login to your **Domain Registrar** (GoDaddy, Namecheap, etc.)
2. Go to **DNS Settings**
3. Add/Update these records:

```
Type: A Record
Name: @
Value: YOUR_VPS_IP
TTL: 3600

Type: A Record  
Name: www
Value: YOUR_VPS_IP
TTL: 3600
```

**⏰ DNS propagation takes 15 minutes to 24 hours**

---

## 💻 **Step 3: Upload Project to Hostinger VPS**

### **Option A: Using WinSCP (Recommended for Windows)**

1. **Download WinSCP:** https://winscp.net/eng/download.php
2. **Install and Open WinSCP**
3. **Connect to VPS:**
   ```
   Host name: YOUR_VPS_IP
   User name: root
   Password: YOUR_VPS_PASSWORD
   ```
4. **Upload Project:**
   - Navigate to `/var/www/` on the right panel
   - Create folder: `school-website`
   - Upload all files from `C:\Users\jvs\Desktop\test` to `/var/www/school-website/`

### **Option B: Using Command Line (Alternative)**

```powershell
# If you have SSH client (Windows 10+)
scp -r C:\Users\jvs\Desktop\test root@YOUR_VPS_IP:/var/www/school-website
```

---

## ⚙️ **Step 4: Prepare Files for Hostinger**

### **Create Hostinger-Specific Environment File:**

Create `.env.hostinger`:
```env
# Hostinger Production Environment
DOMAIN_NAME=yourdomain.com
SECRET_KEY=your-super-secret-key-change-this-now-64-characters-long
DB_PASSWORD=your-strong-database-password-123
ADMIN_URL=secret-admin-panel-xyz/

# Security Settings
DEBUG=False
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True

# Email Settings (Optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

---

## 🐳 **Step 5: Connect to Hostinger VPS and Deploy**

### **Connect via SSH:**

#### **Windows 10+ (Built-in SSH):**
```powershell
ssh root@YOUR_VPS_IP
# Enter your password when prompted
```

#### **Windows (Using PuTTY):**
1. Download PuTTY: https://putty.org/
2. Open PuTTY
3. Enter VPS IP and connect
4. Login with root and password

### **Once Connected to VPS:**

```bash
# Update system
apt update && apt upgrade -y

# Navigate to project
cd /var/www/school-website

# Copy environment file
cp env.production.template .env

# Edit environment file with your details
nano .env
```

**Edit the .env file with:**
```env
DOMAIN_NAME=yourdomain.com
SECRET_KEY=generate-a-random-64-character-key-here
DB_PASSWORD=your-strong-db-password
ADMIN_URL=your-secret-admin-url/
```

**Save and exit:** `Ctrl+X`, then `Y`, then `Enter`

---

## 🚀 **Step 6: Deploy Your Website**

### **Run the Deployment Script:**
```bash
# Make script executable
chmod +x deploy.sh

# Run deployment
./deploy.sh
```

### **What the Script Does:**
- ✅ Installs Docker & Docker Compose
- ✅ Gets SSL certificates (HTTPS)
- ✅ Deploys your website
- ✅ Sets up database
- ✅ Creates admin user
- ✅ Configures backups

### **Script Output:**
```
🚀 Starting production deployment...
📁 Checking required files... ✅
📋 Loading environment variables... ✅
🔧 Updating nginx configuration... ✅
🐳 Installing Docker... ✅
🔒 Setting up SSL certificates... ✅
🚀 Deploying application... ✅
📊 Setting up monitoring... ✅

🎉 Deployment completed successfully!
Your website is now available at: https://yourdomain.com
Admin panel: https://yourdomain.com/your-secret-admin-url/
```

---

## 🔐 **Step 7: Create Admin User**

```bash
# Create your admin account
docker-compose -f docker-compose.prod.yml exec web python manage.py manage_admin_users --create-superuser

# Follow prompts:
Username: admin
Email: your-email@domain.com
Password: (enter secure password)
```

---

## ✅ **Step 8: Verify Deployment**

### **Check Your Website:**
1. **Visit:** `https://yourdomain.com`
2. **Admin Panel:** `https://yourdomain.com/your-secret-admin-url/`
3. **Test Features:**
   - Home page slideshow
   - Gallery
   - Contact form
   - Admin login

### **Check Server Status:**
```bash
# Check running containers
docker-compose -f docker-compose.prod.yml ps

# View logs
docker-compose -f docker-compose.prod.yml logs -f web

# Check resources
htop
```

---

## 🛠️ **Hostinger-Specific Optimizations**

### **Optimize for Single CPU Core:**
```bash
# Create optimization script
cat > optimize_hostinger.sh << 'EOF'
#!/bin/bash
echo "🔧 Optimizing for Hostinger VPS..."

# Reduce swappiness for better performance
echo 'vm.swappiness=10' >> /etc/sysctl.conf
echo 'vm.dirty_ratio=15' >> /etc/sysctl.conf
echo 'vm.dirty_background_ratio=5' >> /etc/sysctl.conf

# Network optimizations
echo 'net.core.rmem_max = 16777216' >> /etc/sysctl.conf
echo 'net.core.wmem_max = 16777216' >> /etc/sysctl.conf

# Apply settings
sysctl -p

# Optimize Docker for single core
cat > /etc/docker/daemon.json << 'EOL'
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  },
  "default-ulimits": {
    "nofile": {
      "Name": "nofile",
      "Hard": 64000,
      "Soft": 64000
    }
  }
}
EOL

systemctl restart docker
echo "✅ Optimization complete!"
EOF

chmod +x optimize_hostinger.sh
./optimize_hostinger.sh
```

### **Setup Monitoring:**
```bash
# Install monitoring tools
apt install htop iotop ncdu -y

# Create monitoring script
cat > monitor.sh << 'EOF'
#!/bin/bash
echo "📊 Hostinger VPS Status:"
echo "========================"
echo "🖥️  CPU Usage:"
top -bn1 | grep "Cpu(s)" | awk '{print $2}' | awk -F'%' '{print $1"%"}'

echo "💾 Memory Usage:"
free -h | awk 'NR==2{printf "%.1f%% (%s/%s)\n", $3*100/$2, $3, $2}'

echo "💿 Disk Usage:"
df -h / | awk 'NR==2{printf "%s (%s used)\n", $5, $3}'

echo "🌐 Website Status:"
curl -s -o /dev/null -w "Response Time: %{time_total}s\nHTTP Code: %{http_code}\n" https://yourdomain.com
EOF

chmod +x monitor.sh
```

---

## 📱 **Step 9: Hostinger Panel Integration**

### **Use Hostinger's Built-in Tools:**

1. **File Manager:**
   - Access via Hostinger Panel
   - Edit files directly in browser
   - Useful for quick changes

2. **Database Access:**
   ```bash
   # Connect to PostgreSQL
   docker-compose -f docker-compose.prod.yml exec db psql -U postgres
   ```

3. **Backup via Hostinger:**
   - Enable automatic backups in Hostinger Panel
   - Download backups monthly

---

## 🔄 **Maintenance & Updates**

### **Weekly Monitoring:**
```bash
# Run monitoring script
./monitor.sh

# Check logs
docker-compose -f docker-compose.prod.yml logs --tail=100 web
```

### **Monthly Updates:**
```bash
# Update system packages
apt update && apt upgrade -y

# Update Docker images
docker-compose -f docker-compose.prod.yml pull
docker-compose -f docker-compose.prod.yml up -d

# Backup database
docker-compose -f docker-compose.prod.yml exec db pg_dump -U postgres postgres > backup_$(date +%Y%m%d).sql
```

### **Content Updates:**
- **Admin Panel:** `https://yourdomain.com/your-admin-url/`
- **Add Photos:** Upload through admin
- **Update Pages:** Edit via admin interface

---

## 🆘 **Troubleshooting**

### **Common Issues:**

#### **1. Website Not Loading:**
```bash
# Check if containers are running
docker-compose -f docker-compose.prod.yml ps

# Restart if needed
docker-compose -f docker-compose.prod.yml restart
```

#### **2. SSL Certificate Issues:**
```bash
# Renew certificates
certbot renew

# Restart nginx
docker-compose -f docker-compose.prod.yml restart nginx
```

#### **3. Out of Memory:**
```bash
# Check memory usage
free -h

# Restart containers to free memory
docker-compose -f docker-compose.prod.yml restart
```

#### **4. Domain Not Working:**
```bash
# Check DNS propagation
nslookup yourdomain.com

# Wait up to 24 hours for DNS to propagate
```

---

## 💰 **Performance Expectations**

### **Your Hostinger VPS Can Handle:**
- **👥 Concurrent Users:** 200-300
- **📈 Daily Visitors:** 15,000-20,000  
- **⚡ Page Load Time:** 1-2 seconds
- **💾 Storage Used:** ~15GB out of 50GB
- **📊 Bandwidth Used:** ~500GB out of 4TB/month

### **When to Upgrade:**
- **CPU:** Constantly above 80%
- **Memory:** Consistently above 85%
- **Visitors:** More than 25,000 daily
- **Storage:** Above 40GB used

---

## 🎉 **Congratulations!**

Your **Kapadia High School Website** is now live on Hostinger VPS!

### **🌐 Access Points:**
- **Website:** https://yourdomain.com
- **Admin Panel:** https://yourdomain.com/your-secret-admin-url/
- **Hostinger Panel:** https://hpanel.hostinger.com

### **📱 Next Steps:**
1. ✅ Test all website features
2. ✅ Login to admin and add content
3. ✅ Update school information
4. ✅ Upload photos and events
5. ✅ Share with stakeholders

### **🔧 Monthly Tasks:**
- Check website performance
- Backup database
- Update content via admin
- Monitor server resources

**Your website is production-ready and optimized for Hostinger VPS!** 🚀
