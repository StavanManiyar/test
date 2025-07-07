# Detailed Hostinger VPS Hosting Guide for Kapadia High School Project

This guide provides a comprehensive step-by-step process for deploying the Kapadia High School Django application to a VPS on Hostinger.

## Prerequisites

- **VPS Server**: Ubuntu 20.04 or later
- **Domain Name**: Your desired domain name (e.g., kapadiahighschool.com)
- **SSH Access**: Ensure SSH access to your VPS
- **Basic Linux Knowledge**: Understanding of basic Linux commands

## Step 1: Connect to Your VPS via SSH

1. **Log in to your Hostinger account**
   - Go to [Hostinger](https://www.hostinger.com/)
   - Navigate to **Hosting** > **Manage** next to your VPS

2. **Access SSH Terminal**:
   - Find your server's IP address
   - Open a terminal (command prompt) and connect using SSH:
     ```bash
     ssh root@your-vps-ip
     ```

## Step 2: Initial Server Setup

1. **Update System Packages**:
   ```bash
   apt update && apt upgrade -y
   ```

2. **Create a New User** (Recommended):
   ```bash
   adduser kapadiaschool
   usermod -aG sudo kapadiaschool
   su - kapadiaschool
   ```

## Step 3: Install Required Software

1. **Install Python, Nginx, and Dependencies**:
   ```bash
   sudo apt install -y python3 python3-pip python3-venv nginx supervisor git
   ```

2. **Install PostgreSQL** (If using PostgreSQL):
   ```bash
   sudo apt install -y postgresql postgresql-contrib
   ```

## Step 4: Clone and Deploy the Application

1. **Clone Your GitHub Repository**:
   ```bash
   cd /var/www/
   sudo git clone https://github.com/your-username/kapadiaschool.git
   sudo chown -R www-data:www-data kapadiaschool
   cd kapadiaschool
   ```

2. **Run Deployment Script**:
   ```bash
   chmod +x deploy_vps.sh
   sudo ./deploy_vps.sh
   ```

## Step 5: Configure Environment Variables

1. **Create Environment File**:
   ```bash
   sudo nano /var/www/kapadiaschool/.env
   ```

2. **Add Environment Variables**:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=False
   DATABASE_URL=postgres://username:password@localhost/database_name
   VPS_SERVER_IP=your-vps-ip
   ```

## Step 6: Configure Nginx

1. **Copy Nginx Configuration**:
   ```bash
   sudo cp /var/www/kapadiaschool/nginx.conf /etc/nginx/sites-available/kapadiaschool
   sudo ln -s /etc/nginx/sites-available/kapadiaschool /etc/nginx/sites-enabled/
   ```

2. **Remove Default Nginx Site**:
   ```bash
   sudo rm /etc/nginx/sites-enabled/default
   ```

3. **Restart Nginx**:
   ```bash
   sudo systemctl restart nginx
   sudo systemctl enable nginx
   ```

## Step 7: Configure Supervisor

1. **Setup Supervisor**:
   ```bash
   sudo cp /var/www/kapadiaschool/supervisor.conf /etc/supervisor/conf.d/kapadiaschool.conf
   sudo supervisorctl reread
   sudo supervisorctl update
   sudo supervisorctl start kapadiaschool_group:*
   ```

## Step 8: Setup SSL Certificate (Let's Encrypt)

1. **Install Certbot**:
   ```bash
   sudo apt install -y certbot python3-certbot-nginx
   ```

2. **Obtain SSL Certificate**:
   ```bash
   sudo certbot --nginx -d kapadiahighschool.com -d www.kapadiahighschool.com
   ```

3. **Enable Automatic Renewal**:
   ```bash
   sudo crontab -e
   ```
   Add the following line:
   ```
   0 12 * * * /usr/bin/certbot renew --quiet
   ```

## Step 9: Database Configuration (PostgreSQL)

1. **Setup PostgreSQL User and Database**:
   ```bash
   sudo -u postgres psql
   CREATE DATABASE kapadiaschool;
   CREATE USER kapadiaschool_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE kapadiaschool TO kapadiaschool_user;
   \q
   ```

2. **Update Environment File with Database URL**:
   ```env
   DATABASE_URL=postgres://kapadiaschool_user:your_password@localhost/kapadiaschool
   ```

## Step 10: Domain Configuration

1. **Point Domain to VPS IP**:
   - Log in to your domain registrar
   - Set A record for `@` to point to your VPS IP
   - Set A record for `www` to point to your VPS IP

2. **Allow DNS Propagation**:
   - Wait 24-48 hours for changes to take effect

## Step 11: Finalize Setup

1. **Run Database Migrations**:
   ```bash
   cd /var/www/kapadiaschool
   source venv/bin/activate
   python manage.py migrate
   ```

2. **Create Admin Account**:
   ```bash
   python manage.py createsuperuser
   ```

3. **Collect Static Files**:
   ```bash
   python manage.py collectstatic --noinput
   ```

4. **Restart All Services**:
   ```bash
   sudo supervisorctl restart kapadiaschool_group:*
   sudo systemctl restart nginx
   ```

## Monitoring and Maintenance

- **Monitor Logs**:
  ```bash
  sudo tail -f /var/www/kapadiaschool/logs/gunicorn.log
  sudo tail -f /var/log/nginx/kapadiaschool_error.log
  ```

- **Check Application Status**:
  ```bash
  sudo supervisorctl status
  sudo systemctl status nginx
  ```

## Security Hardening

1. **Configure Firewall**:
   ```bash
   sudo ufw allow ssh
   sudo ufw allow 'Nginx Full'
   sudo ufw enable
   ```

2. **Regular Security Updates**:
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

---

Your application should now be securely deployed and operational on your VPS with Hostinger. Verify your setup and ensure regular maintenance for optimal performance!
