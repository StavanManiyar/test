# Kapadia High School Website

A Django-based website for Kapadia High School, showcasing the school's campuses, facilities, and CBSE certification documents.

## Features

- Multiple campus pages (Chandkheda, Chhatral, IFFCO Township, Kadi)
- CBSE certification document access
- Responsive design with Bootstrap
- Campus facilities showcase

## Local Development

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv venv
   ```
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
5. Run migrations:
   ```
   python manage.py migrate
   ```
6. Run the development server:
   ```
   python manage.py runserver
   ```

## Deployment on Render

### Prerequisites

1. Create a [Render](https://render.com/) account
2. Create a new PostgreSQL database on Render
3. Set up Supabase for image storage (recommended for production)

### Deployment Steps

#### Option 1: Manual Deployment

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Configure the following settings:
   - **Name**: kapadia-school (or your preferred name)
   - **Environment**: Python 3
   - **Region**: Choose the region closest to your users
   - **Branch**: main (or your default branch)
   - **Build Command**: `./build.sh`
   - **Start Command**: `python manage.py runserver 0.0.0.0:$PORT`
4. Add the following environment variables:
   - `DEBUG`: false
   - `SECRET_KEY`: (generate a secure random key)
   - `DATABASE_URL`: (your PostgreSQL connection string from Render)
   - `SUPABASE_URL`: (your Supabase project URL)
   - `SUPABASE_KEY`: (your Supabase API key)

#### Option 2: Blueprint Deployment (Recommended)

1. Push the `render.yaml` file to your repository
2. Go to the Render Dashboard and click "Blueprint"
3. Connect to your repository
4. Render will automatically set up the web service and database
5. You'll need to manually add the Supabase environment variables after deployment

### Accessing the Admin Interface

After deployment, the admin interface will be available at `https://your-app-name.onrender.com/admin/`

Default admin credentials (created during deployment):
- Username: `admin`
- Password: `admin@123`

**Important:** Change the default password immediately after your first login for security reasons.

### Using Supabase with Render

This project uses Supabase for storing images (carousel, gallery, etc.) while hosting the application on Render. Here's how to set it up:

1. **Create a Supabase Account and Project**:
   - Sign up at [Supabase](https://supabase.com/)
   - Create a new project
   - Navigate to the Storage section and create buckets for:
     - `carousel` - For carousel images
     - `festival` - For festival gallery images
     - `images` - For general images

2. **Get Your Supabase Credentials**:
   - Go to Project Settings > API
   - Copy the URL and anon/public key
   - Add these to your Render environment variables as `SUPABASE_URL` and `SUPABASE_KEY`

3. **Verify Bucket Creation**:
   - The `initialize_supabase_buckets` management command will run during deployment
   - Check the build logs to confirm successful bucket initialization

4. **Testing Locally**:
   - Add the Supabase credentials to your local `.env` file
   - Run `python manage.py initialize_supabase_buckets` to set up buckets

### Troubleshooting

1. **Database Connection Issues**: Verify your DATABASE_URL environment variable is correct
2. **Static Files Not Loading**: Check if collectstatic ran successfully in the build logs
3. **Admin Interface Not Working**: Ensure migrations completed successfully
4. **500 Server Error**: Check the Render logs for detailed error information
5. **Images Not Loading**: Verify Supabase credentials and bucket initialization in the build logs

Your website will be deployed and available at the URL provided by Render.

## Project Structure

- `kapadiaschool/` - Main project directory
  - `kapadiaschool/` - Project settings
  - `khschool/` - Main app
  - `templates/` - HTML templates
  - `static/` - Static files (CSS, JS, images)
  - `gallery/` - Media files
  - `requirements.txt` - Python dependencies
  - `build.sh` - Build script for Render
  - `Procfile` - Process file for web servers
  - `runtime.txt` - Python version specification

# Kapadia High School Website Deployment Guide

This guide explains how to deploy the Kapadia High School website on Render with PostgreSQL for data storage and Supabase for image storage.

## Prerequisites

- [Render](https://render.com) account
- [Supabase](https://supabase.com) account
- Git repository with your project code

## Step 1: Set Up Supabase for Image Storage

1. **Create a Supabase Project**:
   - Sign in to [Supabase](https://app.supabase.com)
   - Click "New Project"
   - Enter a name for your project
   - Choose a database password
   - Select a region close to your users
   - Click "Create new project"

2. **Create Storage Buckets**:
   - In your Supabase dashboard, go to "Storage"
   - Create the following buckets with exactly these names:
     - `carousel-images` - For homepage carousel images
     - `celebration-images` - For main celebration/festival images
     - `gallery-images` - For gallery photos
     - `gallery-thumbnails` - For gallery thumbnail images

3. **Get API Credentials**:
   - Go to "Settings" > "API"
   - Copy your "Project URL" and "API Key" (anon public)
   - You'll need these for the environment variables later

## Step 2: Create a PostgreSQL Database on Render

1. **Log in to Render**:
   - Sign in to [Render](https://dashboard.render.com)

2. **Create a PostgreSQL Database**:
   - Click "New" > "PostgreSQL"
   - Enter a name (e.g., "kapadia-school-db")
   - Choose a region close to your users
   - Select an appropriate database plan
   - Click "Create Database"

3. **Get Connection Details**:
   - Once created, note the following from the database dashboard:
     - Internal Database URL
     - External Database URL
     - Username
     - Password

## Step 3: Deploy the Web Service on Render

1. **Create a New Web Service**:
   - Click "New" > "Web Service"
   - Connect your Git repository
   - Enter a name (e.g., "kapadia-school-website")
   - Choose "Python" as the runtime
   - Set the build command to: `./build.sh`
   - Set the start command to: `gunicorn kapadiaschool.wsgi:application`

2. **Configure Environment Variables**:
   - In the "Environment" section, add the following variables:
     - `DATABASE_URL`: Your PostgreSQL connection string from Step 2
     - `SUPABASE_URL`: Your Supabase project URL from Step 1
     - `SUPABASE_KEY`: Your Supabase API key from Step 1
     - `SECRET_KEY`: A secure random string for Django
     - `RENDER_EXTERNAL_HOSTNAME`: Your Render service URL (will be auto-populated)
     - `DEBUG`: Set to `False` for production

3. **Set Advanced Options**:
   - Set "Auto-Deploy" to "Yes" if you want automatic deployments
   - Under "Health Check Path", enter `/admin/login/`

4. **Deploy the Service**:
   - Click "Create Web Service"
   - Wait for the deployment to complete

## Step 4: Connect a Custom Domain (Optional)

1. **Add Your Custom Domain**:
   - In your web service dashboard, go to "Settings"
   - Scroll to "Custom Domains"
   - Click "Add Custom Domain"
   - Enter your domain name and follow the instructions

2. **Update DNS Records**:
   - Add the CNAME record provided by Render to your domain's DNS settings
   - Wait for DNS propagation (may take up to 48 hours)

## Step 5: Initial Setup After Deployment

1. **Create Admin User**:
   - Access your service's Shell tab in Render dashboard
   - Run: `python manage.py createsuperuser`
   - Follow the prompts to create an admin account

2. **Access Admin Panel**:
   - Visit `https://your-domain.com/admin/` or `https://your-render-url/admin/`
   - Log in with the superuser credentials

3. **Configure Storage Integration**:
   - In the admin panel, upload images as needed
   - The system will automatically store them in Supabase
   - For each model (Celebration, Gallery, etc.), you can upload images directly
   - Images will be automatically optimized and stored in the appropriate Supabase bucket

## How Image Storage Works

The application uses a hybrid approach for image storage:

1. **Development Mode**: 
   - In development (DEBUG=True), images are stored locally in the `gallery/` directory
   - Local file URLs are prioritized over Supabase URLs

2. **Production Mode**:
   - In production (DEBUG=False), images are stored in Supabase
   - Supabase URLs are prioritized over local file URLs
   - Images are automatically optimized (resized and compressed) before upload
   - The system maintains both local and Supabase references for each image
   - When images are deleted in the admin panel, they are also automatically deleted from Supabase storage

3. **Image Optimization**:
   - Carousel images: 1920×600px
   - Celebration images: 800×600px
   - Gallery images: 1200×800px
   - Gallery thumbnails: 400×300px

## Troubleshooting

### Database Connection Issues
- Verify your `DATABASE_URL` environment variable is correct
- Check that your IP is allowed in Render's database access controls
- Run `python manage.py check_db` to diagnose connection issues

### Image Storage Issues
- Verify your Supabase credentials are correct
- Check bucket permissions in Supabase
- Ensure the storage buckets are created with the exact names listed above
- Check the application logs for any Supabase-related errors

### Deployment Failures
- Check the build logs in Render dashboard
- Ensure all required environment variables are set
- Verify your `build.sh` script is executable (`git update-index --chmod=+x build.sh`)

## Maintenance

### Database Backups
- Render automatically creates daily backups of your PostgreSQL database
- You can create manual backups from the database dashboard

### Code Updates
- Push changes to your Git repository
- If auto-deploy is enabled, Render will automatically deploy the changes
- Otherwise, manually deploy from the Render dashboard

## Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Render Documentation](https://render.com/docs)
- [Supabase Documentation](https://supabase.com/docs)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
