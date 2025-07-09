#!/bin/bash

# Exit on any error
set -e

# Function to wait for database
wait_for_db() {
    echo "Waiting for database connection..."
    
    # Extract database host from DATABASE_URL or use default
    DB_HOST=$(echo $DATABASE_URL | sed 's/.*@\([^:]*\):.*/\1/')
    DB_HOST=${DB_HOST:-host.docker.internal}
    
    echo "Checking database connection to $DB_HOST..."
    
    while ! pg_isready -h $DB_HOST -p 5432 -U postgres; do
        echo "Database is not ready yet. Waiting..."
        sleep 2
    done
    
    echo "Database is ready!"
}

# Function to run Django migrations
run_migrations() {
    echo "Running Django migrations..."
    python manage.py makemigrations
    python manage.py migrate
}

# Function to collect static files
collect_static() {
    echo "Collecting static files..."
    python manage.py collectstatic --noinput
}

# Function to create superuser if it doesn't exist
create_superuser() {
    echo "Creating superuser if it doesn't exist..."
    python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created: admin/admin123')
else:
    print('Superuser already exists')
"
}

# Function to load initial data (if any)
load_initial_data() {
    echo "Loading initial data..."
    # Add any initial data loading commands here
    # python manage.py loaddata initial_data.json
}

# Main execution
main() {
    echo "Starting Django application setup..."
    
    # Wait for database to be ready
    wait_for_db
    
    # Run migrations
    run_migrations
    
    # Collect static files
    collect_static
    
    # Create superuser
    create_superuser
    
    # Load initial data
    load_initial_data
    
    echo "Django application setup completed!"
    
    # Start the Django application
    exec "$@"
}

# Run main function with all arguments
main "$@"
