# 🛠️ Kapadia School VPS Maintenance Guide

This guide covers ongoing maintenance, monitoring, and troubleshooting for your VPS deployment.

## 📅 **Automated Maintenance Schedule**

After running `./setup_cron.sh`, these tasks run automatically:

### **Daily Tasks (Automated):**
- **1:00 AM** - Django session cleanup
- **2:00 AM** - Complete backup (database + files + media)
- **Every 30 min** - Health checks with email alerts

### **Weekly Tasks (Automated):**
- **Sunday 3:00 AM** - Database optimization and indexing
- **Sunday 4:00 AM** - Log rotation

### **Monthly Tasks (Automated):**
- **12th at 12:00 PM** - SSL certificate renewal check

## 🔧 **Manual Maintenance Commands**

### **Health Monitoring:**
```bash
# Run comprehensive health check
./health_check.sh

# Check specific services
sudo systemctl status nginx
sudo systemctl status postgresql
sudo supervisorctl status

# Check application logs
sudo tail -f /var/www/kapadiaschool/logs/gunicorn.log
sudo tail -f /var/log/nginx/kapadiaschool_error.log
```

### **Database Maintenance:**
```bash
# Optimize database performance
python manage.py optimize_db --analyze --create-indexes

# Run Django maintenance
python manage.py clearsessions
python manage.py check
python manage.py migrate
```

### **Backup Management:**
```bash
# Create manual backup
./backup_script.sh

# List available backups
ls -la /var/backups/kapadiaschool/

# Restore from backup (example)
cd /var/www/kapadiaschool
source venv/bin/activate
psql kapadiaschool < /var/backups/kapadiaschool/db_backup_YYYYMMDD_HHMMSS.sql
```

### **Security Updates:**
```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Update Python packages
cd /var/www/kapadiaschool
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt --upgrade

# Restart services after updates
sudo supervisorctl restart kapadiaschool_group:*
sudo systemctl restart nginx
```

## 📊 **Performance Monitoring**

### **Resource Usage:**
```bash
# Check disk space
df -h

# Check memory usage
free -h

# Check CPU usage
top

# Check active connections
netstat -an | grep :80 | wc -l
```

### **Database Performance:**
```bash
# Analyze database performance
python manage.py optimize_db --analyze

# Check PostgreSQL stats
sudo -u postgres psql -c "SELECT * FROM pg_stat_activity;"

# Check slow queries (if logging enabled)
sudo tail /var/log/postgresql/postgresql-*.log | grep "slow"
```

### **Application Performance:**
```bash
# Check Django performance
python manage.py check --deploy

# Monitor Gunicorn workers
sudo supervisorctl tail -f kapadiaschool

# Check for memory leaks
ps aux | grep gunicorn
```

## 🚨 **Troubleshooting Guide**

### **Website Not Loading:**
1. **Check services:**
   ```bash
   sudo systemctl status nginx
   sudo supervisorctl status kapadiaschool
   ```

2. **Check logs:**
   ```bash
   sudo tail -f /var/log/nginx/kapadiaschool_error.log
   sudo supervisorctl tail -f kapadiaschool
   ```

3. **Restart services:**
   ```bash
   sudo supervisorctl restart kapadiaschool_group:*
   sudo systemctl restart nginx
   ```

### **Database Connection Issues:**
1. **Check PostgreSQL:**
   ```bash
   sudo systemctl status postgresql
   sudo -u postgres psql -c "\l"
   ```

2. **Test Django connection:**
   ```bash
   python manage.py shell -c "from django.db import connection; cursor = connection.cursor(); print('OK')"
   ```

3. **Check database configuration:**
   ```bash
   grep DATABASE_URL /var/www/kapadiaschool/.env
   ```

### **SSL Certificate Issues:**
1. **Check certificate status:**
   ```bash
   sudo certbot certificates
   ```

2. **Renew certificate:**
   ```bash
   sudo certbot renew --dry-run
   sudo certbot renew
   ```

3. **Check Nginx SSL configuration:**
   ```bash
   sudo nginx -t
   ```

### **High Resource Usage:**
1. **Identify resource hogs:**
   ```bash
   sudo iotop  # Disk usage
   sudo htop   # CPU/Memory usage
   ```

2. **Optimize database:**
   ```bash
   python manage.py optimize_db
   ```

3. **Adjust Gunicorn workers:**
   ```bash
   # Edit supervisor configuration
   sudo nano /etc/supervisor/conf.d/kapadiaschool.conf
   # Restart after changes
   sudo supervisorctl restart kapadiaschool
   ```

## 📧 **Email Alert Setup**

### **Configure Email Notifications:**
1. **Install mail utilities:**
   ```bash
   sudo apt install mailutils
   ```

2. **Configure SMTP (example with Gmail):**
   ```bash
   sudo nano /etc/postfix/main.cf
   ```
   Add:
   ```
   relayhost = [smtp.gmail.com]:587
   smtp_use_tls = yes
   smtp_sasl_auth_enable = yes
   smtp_sasl_password_maps = hash:/etc/postfix/sasl_passwd
   smtp_tls_CAfile = /etc/ssl/certs/ca-certificates.crt
   ```

3. **Test email:**
   ```bash
   echo "Test email from Kapadia School VPS" | mail -s "Test" admin@kapadiaschool.com
   ```

## 🔄 **Update Procedures**

### **Application Updates:**
```bash
# Use the automated update script
./update_app.sh

# Or manual process:
cd /var/www/kapadiaschool
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo supervisorctl restart kapadiaschool_group:*
```

### **System Updates:**
```bash
# Monthly system updates
sudo apt update && sudo apt upgrade -y
sudo apt autoremove -y

# Reboot if kernel updated
sudo reboot
```

## 📈 **Scaling Considerations**

### **When to Scale:**
- **CPU usage** consistently > 80%
- **Memory usage** consistently > 85%
- **Disk usage** > 85%
- **Response time** > 3 seconds

### **Scaling Options:**
1. **Vertical Scaling (Upgrade VPS):**
   - More CPU cores
   - More RAM
   - More storage

2. **Horizontal Scaling (Advanced):**
   - Load balancer
   - Multiple VPS instances
   - Database clustering

3. **Performance Optimization:**
   - Enable caching
   - Optimize database queries
   - Use CDN for static files

## 🛡️ **Security Checklist**

### **Monthly Security Tasks:**
- [ ] Review access logs for suspicious activity
- [ ] Update all software packages
- [ ] Check SSL certificate expiration
- [ ] Review user accounts and permissions
- [ ] Backup security configurations

### **Security Monitoring:**
```bash
# Check for failed login attempts
sudo grep "Failed password" /var/log/auth.log

# Check for suspicious network activity
sudo netstat -an | grep ESTABLISHED

# Monitor file changes (install aide)
sudo apt install aide
sudo aide --init
sudo aide --check
```

## 📞 **Emergency Procedures**

### **Website Down:**
1. Run health check: `./health_check.sh`
2. Check service status: `sudo supervisorctl status`
3. Restart services: `sudo supervisorctl restart kapadiaschool_group:*`
4. Check logs for errors
5. Contact technical support if needed

### **Data Loss:**
1. Stop all services: `sudo supervisorctl stop kapadiaschool_group:*`
2. Restore from latest backup
3. Test restoration thoroughly
4. Restart services
5. Verify website functionality

## 📚 **Useful Commands Reference**

```bash
# Quick status check
sudo supervisorctl status && sudo systemctl status nginx && df -h

# View all logs
sudo tail -f /var/www/kapadiaschool/logs/*.log

# Django shell
python manage.py shell

# Create Django superuser
python manage.py createsuperuser

# Run Django tests
python manage.py test

# Check Django configuration
python manage.py check --deploy
```

Remember: **When in doubt, check the logs first!** Most issues can be diagnosed by examining the application and system logs.

For additional support, consult the README.md and VPS_HOSTINGER_DEPLOYMENT_GUIDE.md files.
