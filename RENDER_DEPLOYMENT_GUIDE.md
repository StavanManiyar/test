# Deploying to Render with Supabase Integration

This guide will walk you through deploying your Kapadia High School Django application to Render while using Supabase for database and storage.

## Prerequisites

1. A [Render](https://render.com/) account
2. Your existing [Supabase](https://supabase.com/) project with:
   - Database already set up
   - Storage buckets created with proper policies
   - API keys and URL

## Step 1: Prepare Your Project for Deployment

### Create a `requirements.txt` file

Make sure your project has a `requirements.txt` file listing all dependencies:

```
django>=4.0.0
pillow
python-dotenv
psycopg2-binary
dj-database-url
whitenoise
gunicorn
supabase
python-slugify
requests
```

### Create a `build.sh` script

Create a file named `build.sh` in your project root:

```bash
#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
```

Make it executable:
```bash
chmod +x build.sh
```

### Update `settings.py` for Production

Ensure your `settings.py` has the following configurations:

```python
import os
import dj_database_url
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-default-secret-key-for-dev')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Add render.com domain to allowed hosts
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

# Default database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Override database with DATABASE_URL environment variable if available
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    DATABASES['default'] = dj_database_url.config(
        default=DATABASE_URL,
        conn_max_age=600,
        conn_health_checks=True,
    )

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Use WhiteNoise for serving static files
MIDDLEWARE = [
    # Add WhiteNoise middleware after SecurityMiddleware
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # ... other middleware
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Supabase configuration
SUPABASE_URL = os.environ.get('SUPABASE_URL', '')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY', '')
```

## Step 2: Create a Render Web Service

1. Log in to your [Render Dashboard](https://dashboard.render.com/)
2. Click **New** and select **Web Service**
3. Connect your GitHub repository or use the manual deploy option
4. Fill in the following details:
   - **Name**: `kapadia-high-school` (or your preferred name)
   - **Environment**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn kapadiaschool.wsgi:application`
   - **Instance Type**: Choose the appropriate plan (Free tier is fine for testing)

## Step 3: Configure Environment Variables

In your Render web service settings, add the following environment variables:

- `DEBUG`: `False`
- `SECRET_KEY`: Generate a secure random key
- `ALLOWED_HOSTS`: `yourdomain.render.com,yourdomain.com` (include your Render URL and custom domain if any)
- `SUPABASE_URL`: Your Supabase project URL
- `SUPABASE_KEY`: Your Supabase anon/public key
- `DATABASE_URL`: Your Supabase PostgreSQL connection string

## Step 4: Connect to Supabase Database

1. In your Supabase project dashboard, go to **Project Settings** > **Database**
2. Find the **Connection String** section and select **URI**
3. Copy the connection string and replace `[YOUR-PASSWORD]` with your database password
4. Use this as your `DATABASE_URL` environment variable in Render

## Step 5: Deploy Your Application

1. Click **Create Web Service** in Render
2. Wait for the build and deployment process to complete
3. Once deployed, click the generated URL to view your application

## Step 6: Verify Supabase Integration

1. Check that your application can connect to Supabase storage
2. Verify that image uploads and deletions work correctly
3. Confirm that database queries are functioning properly

## Troubleshooting

### Database Connection Issues

If you encounter database connection problems:

1. Verify your `DATABASE_URL` is correct
2. Check Supabase IP allow list settings
3. Ensure your database password is correctly included in the connection string

### Storage Access Issues

If images aren't loading or can't be uploaded:

1. Verify your `SUPABASE_URL` and `SUPABASE_KEY` environment variables
2. Check bucket policies in Supabase to ensure proper access
3. Look for CORS configuration issues

### Deployment Failures

If your deployment fails:

1. Check the build logs in Render for specific errors
2. Verify all required dependencies are in your `requirements.txt`
3. Ensure your `build.sh` script is executable

## Maintenance

### Updating Your Application

To update your application:

1. Push changes to your connected GitHub repository, or
2. Manually deploy a new version through the Render dashboard

### Database Backups

Supabase automatically creates daily backups of your database. You can also:

1. Go to the SQL Editor in Supabase
2. Create and run export queries
3. Save the results for manual backups

### Monitoring

Monitor your application's performance using:

1. Render's built-in logs and metrics
2. Supabase's database insights
3. Consider adding application monitoring like Sentry
