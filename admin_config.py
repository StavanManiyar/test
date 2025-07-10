#!/usr/bin/env python
"""
Admin Configuration Script
This script helps configure admin access and secure URLs
"""
import os
import subprocess
import sys

def show_current_config():
    """Show current admin configuration"""
    print("Current Admin Configuration:")
    print("=" * 50)
    
    # Check environment variables
    admin_url = os.environ.get('ADMIN_URL', 'khs-secure-admin-2024/')
    debug = os.environ.get('DEBUG', 'False')
    
    print(f"ADMIN_URL: {admin_url}")
    print(f"DEBUG: {debug}")
    print()
    
    # Show access URLs
    if admin_url == 'admin/':
        print("Admin Panel Access:")
        print("- Standard URL: http://localhost/admin/")
        print("- Direct Django: http://localhost:8000/admin/")
    else:
        print("Admin Panel Access:")
        print(f"- Secure URL: http://localhost/{admin_url}")
        print(f"- Direct Django: http://localhost:8000/{admin_url}")
        print("- Standard /admin/ is also available (fallback)")
    print()

def change_admin_url():
    """Change the admin URL configuration"""
    print("Change Admin URL Configuration:")
    print("=" * 50)
    
    print("Options:")
    print("1. Use standard /admin/ (less secure, easier to remember)")
    print("2. Use secure custom URL (more secure, harder to guess)")
    print("3. Generate random secure URL")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == '1':
        new_admin_url = 'admin/'
    elif choice == '2':
        new_admin_url = input("Enter custom admin URL (e.g., 'my-secret-admin/'): ").strip()
        if not new_admin_url.endswith('/'):
            new_admin_url += '/'
    elif choice == '3':
        import secrets
        import string
        # Generate a random secure URL
        random_part = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(16))
        new_admin_url = f'admin-{random_part}/'
    else:
        print("Invalid choice!")
        return
    
    # Update docker-compose.yml
    update_docker_compose_admin_url(new_admin_url)
    
    print(f"\nAdmin URL updated to: {new_admin_url}")
    print("You need to restart the containers for changes to take effect:")
    print("  docker-compose down")
    print("  docker-compose up -d")
    print()

def update_docker_compose_admin_url(new_admin_url):
    """Update ADMIN_URL in docker-compose.yml"""
    docker_compose_file = 'docker-compose.yml'
    
    if not os.path.exists(docker_compose_file):
        print(f"Error: {docker_compose_file} not found!")
        return
    
    # Read the file
    with open(docker_compose_file, 'r') as f:
        content = f.read()
    
    # Replace the ADMIN_URL line
    lines = content.split('\n')
    updated_lines = []
    
    for line in lines:
        if '- ADMIN_URL=' in line:
            # Replace the admin URL
            updated_lines.append(f'      - ADMIN_URL={new_admin_url}')
        else:
            updated_lines.append(line)
    
    # Write back to file
    with open(docker_compose_file, 'w') as f:
        f.write('\n'.join(updated_lines))
    
    print(f"Updated {docker_compose_file} with new ADMIN_URL: {new_admin_url}")

def manage_admin_users():
    """Manage admin users"""
    print("Admin User Management:")
    print("=" * 50)
    
    print("Available actions:")
    print("1. List all users")
    print("2. Create new superuser")
    print("3. Reset user password")
    print("4. Deactivate user")
    print("5. Activate user")
    
    choice = input("\nEnter your choice (1-5): ").strip()
    
    commands = {
        '1': 'docker-compose exec web python manage.py manage_admin_users --list-users',
        '2': 'docker-compose exec web python manage.py manage_admin_users --create-superuser',
        '3': None,  # Special handling needed
        '4': None,  # Special handling needed
        '5': None,  # Special handling needed
    }
    
    if choice in ['1', '2']:
        print(f"\nRunning: {commands[choice]}")
        os.system(commands[choice])
    elif choice == '3':
        username = input("Enter username to reset password: ").strip()
        cmd = f'docker-compose exec web python manage.py manage_admin_users --reset-password {username}'
        print(f"\nRunning: {cmd}")
        os.system(cmd)
    elif choice == '4':
        username = input("Enter username to deactivate: ").strip()
        cmd = f'docker-compose exec web python manage.py manage_admin_users --deactivate-user {username}'
        print(f"\nRunning: {cmd}")
        os.system(cmd)
    elif choice == '5':
        username = input("Enter username to activate: ").strip()
        cmd = f'docker-compose exec web python manage.py manage_admin_users --activate-user {username}'
        print(f"\nRunning: {cmd}")
        os.system(cmd)
    else:
        print("Invalid choice!")

def test_admin_access():
    """Test admin panel access"""
    print("Testing Admin Panel Access:")
    print("=" * 50)
    
    print("Running comprehensive admin test...")
    os.system('python test_admin.py')

def main():
    """Main menu"""
    while True:
        print("\nDjango Admin Configuration Tool")
        print("=" * 50)
        print("1. Show current configuration")
        print("2. Change admin URL")
        print("3. Manage admin users")
        print("4. Test admin access")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            show_current_config()
        elif choice == '2':
            change_admin_url()
        elif choice == '3':
            manage_admin_users()
        elif choice == '4':
            test_admin_access()
        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
