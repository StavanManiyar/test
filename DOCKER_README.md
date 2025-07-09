# Docker Setup for Kapadia School Project

This guide will help you set up and test your Django project locally using Docker, simulating the VPS environment before you purchase hosting.

## Prerequisites

1. **Docker Desktop** (for Windows)
   - Download and install Docker Desktop from https://www.docker.com/products/docker-desktop/
   - Make sure Docker is running

2. **Git** (if not already installed)
   - Download from https://git-scm.com/downloads

## Quick Start

1. **Clone or navigate to your project directory**
   ```bash
   cd C:\Users\jvs\Desktop\test
   ```

2. **Build and run the containers**
   ```bash
   docker-compose up --build
   ```

3. **Wait for the setup to complete**
   - The setup will automatically:
     - Install dependencies
     - Set up PostgreSQL database
     - Run migrations
     - Collect static files
     - Create a superuser (admin/admin123)

4. **Access your application**
   - Website: http://localhost:8000
   - Admin Panel: http://localhost:8000/admin (admin/admin123)

## What's Included

### Services
- **web**: Django application running on Gunicorn
- **db**: PostgreSQL 15.3 database

### Features
- ✅ PostgreSQL database (same as VPS)
- ✅ Gunicorn WSGI server (production-ready)
- ✅ Static file serving
- ✅ Media file handling
- ✅ Automatic migrations
- ✅ Superuser creation
- ✅ Health checks
- ✅ Persistent volumes for database

## Useful Commands

### Start the application
```bash
docker-compose up
```

### Start in background (detached mode)
```bash
docker-compose up -d
```

### Stop the application
```bash
docker-compose down
```

### View logs
```bash
docker-compose logs -f
```

### View logs for specific service
```bash
docker-compose logs -f web
docker-compose logs -f db
```

### Rebuild containers
```bash
docker-compose up --build
```

### Access Django shell
```bash
docker-compose exec web python manage.py shell
```

### Run Django management commands
```bash
docker-compose exec web python manage.py collectstatic
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

### Access PostgreSQL database
```bash
docker-compose exec db psql -U postgres -d kapadiaschool
```

## Database Information

- **Database**: PostgreSQL 15.3
- **Host**: db (internal Docker network)
- **Port**: 5432
- **Username**: postgres
- **Password**: postgres
- **Database Name**: kapadiaschool

## File Structure

```
├── Dockerfile              # Docker image configuration
├── docker-compose.yml      # Multi-container application setup
├── entrypoint.sh           # Container initialization script
├── .dockerignore           # Files to exclude from Docker build
├── .env.docker            # Environment variables for Docker
└── DOCKER_README.md       # This file
```

## Environment Variables

Key environment variables set in the Docker environment:

- `DEBUG=False` - Production mode
- `SECRET_KEY` - Django secret key
- `DATABASE_URL` - PostgreSQL connection string
- `VPS_SERVER_IP=127.0.0.1` - Local development IP

## Troubleshooting

### Container won't start
```bash
# Check logs
docker-compose logs -f

# Remove containers and volumes, then rebuild
docker-compose down -v
docker-compose up --build
```

### Database connection errors
```bash
# Check if database is running
docker-compose ps

# Restart database service
docker-compose restart db
```

### Permission errors
```bash
# On Windows, make sure Docker Desktop is running as administrator
# Check Docker Desktop settings for file sharing permissions
```

### Port already in use
```bash
# Check what's using port 8000
netstat -ano | findstr :8000

# Stop the process or change port in docker-compose.yml
```

## Performance Testing

Once your application is running, you can test its performance:

1. **Load Testing** (using browser or tools like JMeter)
2. **Database Performance** - Check query performance
3. **Static File Serving** - Test CSS/JS/Image loading
4. **Memory Usage** - Monitor container resources

## Production Readiness Checklist

Before deploying to VPS:

- [ ] Application starts without errors
- [ ] Database migrations run successfully
- [ ] Static files are served correctly
- [ ] Media files upload and display properly
- [ ] Admin interface works
- [ ] All pages load without errors
- [ ] Form submissions work
- [ ] Error handling works properly

## Stopping and Cleanup

### Stop containers
```bash
docker-compose down
```

### Remove containers and volumes (complete cleanup)
```bash
docker-compose down -v
```

### Remove Docker images
```bash
docker rmi test-web
docker rmi postgres:15.3
```

## Next Steps

Once you've tested your application successfully:

1. **Purchase VPS hosting** (Hostinger or similar)
2. **Set up production environment** using similar configuration
3. **Configure domain and SSL** 
4. **Set up monitoring and backups**

## Support

If you encounter issues:
1. Check the logs: `docker-compose logs -f`
2. Verify Docker is running
3. Check port availability
4. Ensure all files are in the correct location

---

**Note**: This Docker setup closely mimics your VPS environment, giving you confidence that your application will work properly when deployed to actual hosting.
