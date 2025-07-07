# Kapadia High School Website

![Kapadia High School](static/image/khes.png)

A comprehensive Django web application for Kapadia High School featuring gallery management, admin panel, and responsive design optimized for VPS hosting on Hostinger.

## 🌟 Features

- **Responsive Design**: Mobile-first approach with Bootstrap 5
- **Image Gallery**: Dynamic gallery with Supabase cloud storage integration
- **Admin Panel**: Full-featured Django admin interface
- **SEO Optimized**: Meta tags, sitemaps, and structured data
- **Performance**: Optimized with caching, compression, and CDN-ready
- **Security**: HTTPS, CSRF protection, and security headers
- **VPS Ready**: Configured for production deployment on Hostinger VPS

## 🛠️ Technology Stack

- **Backend**: Django 5.2.1, Python 3.11
- **Database**: PostgreSQL (Production), SQLite (Development)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Web Server**: Nginx + Gunicorn
- **Process Management**: Supervisor
- **Storage**: Supabase (Images), Local filesystem (Static files)
- **Caching**: Django Cache Framework
- **SSL**: Let's Encrypt

## 📋 Prerequisites

Before deploying to VPS, ensure you have:

- VPS server with Ubuntu 20.04+ (Hostinger VPS recommended)
- Domain name pointed to your VPS IP
- SSH access to your VPS
- Basic knowledge of Linux commands
- Git installed on your VPS

## 🚀 Quick Start - VPS Deployment on Hostinger

### Step 1: Purchase and Setup VPS on Hostinger

1. **Purchase VPS Plan:**
   - Visit [Hostinger VPS](https://www.hostinger.com/vps-hosting)
   - Choose a plan (Start VPS or Business VPS recommended)
   - Complete the purchase

2. **Access VPS:**
   - Log into Hostinger hPanel
   - Go to VPS section
   - Note your server IP address
   - Set up SSH access (use provided credentials or add SSH key)

3. **Initial Server Setup:**
   ```bash
   # Connect to your VPS
   ssh root@YOUR_VPS_IP
   
   # Update system
   apt update && apt upgrade -y
   
   # Create non-root user (recommended)
   adduser kapadiaschool
   usermod -aG sudo kapadiaschool
   su - kapadiaschool
   ```

### Step 2: Domain Configuration

1. **Point Domain to VPS:**
   - Log into your domain registrar (or use Hostinger domains)
   - Add DNS records:
     - A record: `@` → `YOUR_VPS_IP`
     - A record: `www` → `YOUR_VPS_IP`
   - Wait for DNS propagation (up to 24 hours)

### Step 3: Deploy Application

1. **Clone Repository:**
   ```bash
   cd /var/www/
   sudo git clone https://github.com/your-username/kapadiaschool.git
   sudo chown -R www-data:www-data kapadiaschool
   cd kapadiaschool
   ```

2. **Run Deployment Script:**
   ```bash
   chmod +x deploy_vps.sh
   sudo ./deploy_vps.sh
   ```

3. **Configure Environment Variables:**
   ```bash
   sudo cp .env.example .env
   sudo nano .env
   ```
   
   Update with your values:
   ```env
   SECRET_KEY=your-generated-secret-key
   DEBUG=False
   DATABASE_URL=postgres://username:password@localhost/database_name
   SUPABASE_URL=your-supabase-url
   SUPABASE_KEY=your-supabase-key
   VPS_SERVER_IP=your-vps-ip
   ```

### Step 4: Configure Services

1. **Setup Nginx:**
   ```bash
   sudo cp nginx.conf /etc/nginx/sites-available/kapadiaschool
   sudo ln -s /etc/nginx/sites-available/kapadiaschool /etc/nginx/sites-enabled/
   sudo rm /etc/nginx/sites-enabled/default
   sudo nginx -t
   sudo systemctl restart nginx
   sudo systemctl enable nginx
   ```

2. **Setup Supervisor:**
   ```bash
   sudo cp supervisor.conf /etc/supervisor/conf.d/kapadiaschool.conf
   sudo nano /etc/supervisor/conf.d/kapadiaschool.conf  # Update SECRET_KEY
   sudo supervisorctl reread
   sudo supervisorctl update
   sudo supervisorctl start kapadiaschool_group:*
   ```

3. **Setup Database:**
   ```bash
   sudo -u postgres psql
   CREATE DATABASE kapadiaschool;
   CREATE USER kapadiaschool_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE kapadiaschool TO kapadiaschool_user;
   \q
   ```

4. **Setup SSL Certificate:**
   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
   ```

### Step 5: Final Configuration

1. **Run Migrations:**
   ```bash
   cd /var/www/kapadiaschool
   source venv/bin/activate
   python manage.py migrate
   python manage.py collectstatic --noinput
   ```

2. **Create Superuser:**
   ```bash
   python manage.py createsuperuser
   ```

3. **Restart Services:**
   ```bash
   sudo supervisorctl restart kapadiaschool_group:*
   sudo systemctl restart nginx
   ```

## 🔧 Local Development Setup

1. **Clone Repository:**
   ```bash
   git clone https://github.com/your-username/kapadiaschool.git
   cd kapadiaschool
   ```

2. **Create Virtual Environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your local settings
   ```

5. **Run Migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create Superuser:**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run Development Server:**
   ```bash
   python manage.py runserver
   ```

## 🗂️ Project Structure

```
kapadiaschool/
├── kapadiaschool/           # Django project settings
│   ├── settings.py          # Main settings file
│   ├── urls.py             # URL routing
│   └── wsgi.py             # WSGI configuration
├── khschool/               # Main Django app
│   ├── models.py           # Database models
│   ├── views.py            # View functions
│   ├── admin.py            # Admin interface
│   └── templates/          # HTML templates
├── static/                 # Static files (CSS, JS, Images)
├── gallery/                # Media files (User uploads)
├── templates/              # Global templates
├── deploy_vps.sh          # VPS deployment script
├── nginx.conf             # Nginx configuration
├── supervisor.conf        # Supervisor configuration
├── requirements.txt       # Python dependencies
└── .env.example          # Environment variables template
```

## 🔐 Security Features

- **HTTPS Enforcement**: Automatic HTTP to HTTPS redirects
- **Security Headers**: HSTS, CSP, XSS protection
- **CSRF Protection**: Django CSRF middleware
- **SQL Injection Protection**: Django ORM
- **File Upload Security**: Type validation and sanitization
- **Admin Protection**: Rate limiting and secure authentication

## 📊 Performance Optimizations

- **Static File Compression**: Gzip compression enabled
- **Image Optimization**: Automatic resizing and format optimization
- **Database Optimization**: Connection pooling and query optimization
- **Caching**: Page and database query caching
- **CDN Ready**: Static files optimized for CDN delivery

## 🔍 Monitoring and Maintenance

### Log Files

```bash
# Application logs
sudo tail -f /var/www/kapadiaschool/logs/gunicorn.log

# Nginx logs
sudo tail -f /var/log/nginx/kapadiaschool_error.log
sudo tail -f /var/log/nginx/kapadiaschool_access.log

# System logs
sudo journalctl -u nginx -f
```

### Service Management

```bash
# Check service status
sudo supervisorctl status
sudo systemctl status nginx

# Restart services
sudo supervisorctl restart kapadiaschool_group:*
sudo systemctl restart nginx

# Reload configuration
sudo nginx -t && sudo systemctl reload nginx
```

### Database Backup

```bash
# Create backup
pg_dump kapadiaschool > backup_$(date +%Y%m%d).sql

# Restore backup
psql kapadiaschool < backup_20240101.sql
```

### Update Application

```bash
cd /var/www/kapadiaschool
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo supervisorctl restart kapadiaschool_group:*
```

## 🐛 Troubleshooting

### Common Issues

1. **Application won't start:**
   - Check logs: `sudo supervisorctl tail -f kapadiaschool`
   - Verify environment variables in `.env`
   - Check database connection

2. **Static files not loading:**
   - Run: `python manage.py collectstatic --noinput`
   - Check Nginx configuration
   - Verify file permissions

3. **Images not displaying:**
   - Check media directory permissions
   - Verify Supabase configuration
   - Check gallery directory structure

4. **Database connection errors:**
   - Verify PostgreSQL is running: `sudo systemctl status postgresql`
   - Check database credentials in `.env`
   - Ensure database and user exist

### Performance Issues

1. **Slow page loads:**
   - Enable caching in settings
   - Optimize database queries
   - Use CDN for static files

2. **High memory usage:**
   - Adjust Gunicorn worker count
   - Monitor with `htop`
   - Check for memory leaks

## 📞 Support

For technical support:
- **Email**: admin@kapadiaschool.com
- **Issues**: Create GitHub issue
- **Documentation**: Check `VPS_HOSTINGER_DEPLOYMENT_GUIDE.md`

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📈 Changelog

### Version 2.0.0 (Current)
- ✅ VPS deployment support
- ✅ Nginx + Gunicorn setup
- ✅ SSL certificate automation
- ✅ Performance optimizations
- ✅ Enhanced security features
- ✅ Improved admin interface
- ✅ Larger logo design

### Version 1.0.0
- ✅ Basic Django application
- ✅ Gallery functionality
- ✅ Supabase integration
- ✅ Responsive design

---

**Built with ❤️ for Kapadia High School**

For detailed deployment instructions, see [VPS_HOSTINGER_DEPLOYMENT_GUIDE.md](VPS_HOSTINGER_DEPLOYMENT_GUIDE.md)
