# VPS Hostinger Deployment Guide

This guide will help you deploy the Kapadia School Django application to a VPS server on Hostinger.

## Prerequisites

- VPS server with Ubuntu 20.04 or later
- Domain name (kapadiahighschool.com)
- SSH access to your VPS
- Basic knowledge of Linux commands

## Step 1: Initial Server Setup

1. **Connect to your VPS via SSH:**
   ```bash
   ssh root@your-vps-ip
   ```

2. **Update the system:**
   ```bash
   apt update && apt upgrade -y
   ```

3. **Create a new user (optional but recommended):**
   ```bash
   adduser kapadiaschool
   usermod -aG sudo kapadiaschool
   su - kapadiaschool
   ```

## Step 2: Install Required Software

1. **Install Python, Nginx, and other dependencies:**
   ```bash
   sudo apt install -y python3 python3-pip python3-venv nginx supervisor git
   ```

2. **Install PostgreSQL (if using PostgreSQL):**
   ```bash
   sudo apt install -y postgresql postgresql-contrib
   ```

## Step 3: Deploy the Application

1. **Clone your repository:**
   ```bash
   cd /var/www/
   sudo git clone https://github.com/your-username/kapadiaschool.git
   sudo chown -R www-data:www-data kapadiaschool
   cd kapadiaschool
   ```

2. **Run the deployment script:**
   ```bash
   chmod +x deploy_vps.sh
   sudo ./deploy_vps.sh
   ```

## Step 4: Configure Environment Variables

1. **Create environment file:**
   ```bash
   sudo nano /var/www/kapadiaschool/.env
   ```

2. **Add the following variables:**
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=False
   DATABASE_URL=postgres://username:password@localhost/database_name
   VPS_SERVER_IP=your-vps-ip
   
   # Optional: Only if you want to use Supabase cloud storage
   # SUPABASE_URL=your-supabase-url
   # SUPABASE_KEY=your-supabase-key
   # FORCE_SUPABASE=true
   ```

## Step 5: Configure Nginx

1. **Copy the Nginx configuration:**
   ```bash
   sudo cp /var/www/kapadiaschool/nginx.conf /etc/nginx/sites-available/kapadiaschool
   sudo ln -s /etc/nginx/sites-available/kapadiaschool /etc/nginx/sites-enabled/
   ```

2. **Remove the default Nginx site:**
   ```bash
   sudo rm /etc/nginx/sites-enabled/default
   ```

3. **Test Nginx configuration:**
   ```bash
   sudo nginx -t
   ```

4. **Restart Nginx:**
   ```bash
   sudo systemctl restart nginx
   sudo systemctl enable nginx
   ```

## Step 6: Configure Supervisor

1. **Copy the Supervisor configuration:**
   ```bash
   sudo cp /var/www/kapadiaschool/supervisor.conf /etc/supervisor/conf.d/kapadiaschool.conf
   ```

2. **Update the SECRET_KEY in supervisor.conf:**
   ```bash
   sudo nano /etc/supervisor/conf.d/kapadiaschool.conf
   ```

3. **Reload Supervisor:**
   ```bash
   sudo supervisorctl reread
   sudo supervisorctl update
   sudo supervisorctl start kapadiaschool_group:*
   ```

## Step 7: Set up SSL Certificate (Let's Encrypt)

1. **Install Certbot:**
   ```bash
   sudo apt install -y certbot python3-certbot-nginx
   ```

2. **Obtain SSL certificate:**
   ```bash
   sudo certbot --nginx -d kapadiahighschool.com -d www.kapadiahighschool.com
   ```

3. **Set up automatic renewal:**
   ```bash
   sudo crontab -e
   ```
   Add this line:
   ```
   0 12 * * * /usr/bin/certbot renew --quiet
   ```

## Step 8: Configure Database (PostgreSQL)

1. **Create database and user:**
   ```bash
   sudo -u postgres psql
   CREATE DATABASE kapadiaschool;
   CREATE USER kapadiaschool_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE kapadiaschool TO kapadiaschool_user;
   \q
   ```

2. **Update DATABASE_URL in .env file:**
   ```env
   DATABASE_URL=postgres://kapadiaschool_user:your_password@localhost/kapadiaschool
   ```

## Step 9: Domain Configuration

1. **Point your domain to the VPS IP:**
   - Log in to your domain registrar
   - Add A record: `@` pointing to your VPS IP
   - Add A record: `www` pointing to your VPS IP

2. **Wait for DNS propagation (24-48 hours)**

## Step 10: Final Steps

1. **Run migrations:**
   ```bash
   cd /var/www/kapadiaschool
   source venv/bin/activate
   python manage.py migrate
   ```

2. **Create superuser:**
   ```bash
   python manage.py createsuperuser
   ```

3. **Collect static files:**
   ```bash
   python manage.py collectstatic --noinput
   ```

4. **Restart services:**
   ```bash
   sudo supervisorctl restart kapadiaschool_group:*
   sudo systemctl restart nginx
   ```

## Monitoring and Maintenance

1. **Check application logs:**
   ```bash
   sudo tail -f /var/www/kapadiaschool/logs/gunicorn.log
   ```

2. **Check Nginx logs:**
   ```bash
   sudo tail -f /var/log/nginx/kapadiaschool_error.log
   ```

3. **Monitor services:**
   ```bash
   sudo supervisorctl status
   sudo systemctl status nginx
   ```

## Troubleshooting

1. **If the application doesn't start:**
   - Check logs: `sudo supervisorctl tail -f kapadiaschool`
   - Verify environment variables in .env file
   - Check database connection

2. **If static files don't load:**
   - Run: `python manage.py collectstatic --noinput`
   - Check Nginx configuration for static file serving

3. **If images don't display:**
   - Check media directory permissions
   - Verify Supabase configuration if using Supabase storage

## Security Considerations

1. **Firewall setup:**
   ```bash
   sudo ufw allow ssh
   sudo ufw allow 'Nginx Full'
   sudo ufw enable
   ```

2. **Regular updates:**
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

3. **Monitor logs regularly for suspicious activity**

## Backup Strategy

1. **Database backup:**
   ```bash
   pg_dump kapadiaschool > backup_$(date +%Y%m%d).sql
   ```

2. **Application backup:**
   ```bash
   tar -czf kapadiaschool_backup_$(date +%Y%m%d).tar.gz /var/www/kapadiaschool
   ```

Your Django application should now be successfully deployed on your VPS Hostinger server!
