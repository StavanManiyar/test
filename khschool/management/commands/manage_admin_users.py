from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import transaction
import getpass

class Command(BaseCommand):
    help = 'Safe management of admin users without using web interface'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--create-superuser',
            action='store_true',
            help='Create a new superuser',
        )
        parser.add_argument(
            '--list-users',
            action='store_true',
            help='List all users',
        )
        parser.add_argument(
            '--reset-password',
            type=str,
            help='Reset password for specified username',
        )
        parser.add_argument(
            '--deactivate-user',
            type=str,
            help='Deactivate specified user (safer than deletion)',
        )
        parser.add_argument(
            '--activate-user',
            type=str,
            help='Activate specified user',
        )
        parser.add_argument(
            '--backup-users',
            action='store_true',
            help='Create a backup of user data',
        )
    
    def handle(self, *args, **options):
        if options['create_superuser']:
            self.create_superuser()
        elif options['list_users']:
            self.list_users()
        elif options['reset_password']:
            self.reset_password(options['reset_password'])
        elif options['deactivate_user']:
            self.deactivate_user(options['deactivate_user'])
        elif options['activate_user']:
            self.activate_user(options['activate_user'])
        elif options['backup_users']:
            self.backup_users()
        else:
            self.stdout.write(self.style.ERROR('Please specify an action. Use --help for options.'))
    
    def create_superuser(self):
        """Create a new superuser safely"""
        self.stdout.write(self.style.WARNING('Creating a new superuser...'))
        
        username = input('Username: ')
        email = input('Email: ')
        
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.ERROR(f'User {username} already exists!'))
            return
        
        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.WARNING(f'Email {email} is already in use!'))
            confirm = input('Continue anyway? (y/N): ')
            if confirm.lower() != 'y':
                return
        
        password = getpass.getpass('Password: ')
        password_confirm = getpass.getpass('Confirm password: ')
        
        if password != password_confirm:
            self.stdout.write(self.style.ERROR('Passwords do not match!'))
            return
        
        try:
            with transaction.atomic():
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    is_staff=True,
                    is_superuser=True
                )
                self.stdout.write(
                    self.style.SUCCESS(f'Superuser {username} created successfully!')
                )
        except ValidationError as e:
            self.stdout.write(self.style.ERROR(f'Error creating user: {e}'))
    
    def list_users(self):
        """List all users with their status"""
        self.stdout.write(self.style.SUCCESS('User List:'))
        self.stdout.write('-' * 70)
        
        for user in User.objects.all().order_by('username'):
            status = []
            if user.is_superuser:
                status.append('SUPERUSER')
            if user.is_staff:
                status.append('STAFF')
            if not user.is_active:
                status.append('INACTIVE')
            
            status_str = ', '.join(status) if status else 'REGULAR'
            
            self.stdout.write(
                f'{user.username:<20} {user.email:<30} {status_str}'
            )
    
    def reset_password(self, username):
        """Reset password for a user"""
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User {username} not found!'))
            return
        
        self.stdout.write(f'Resetting password for user: {username}')
        
        password = getpass.getpass('New password: ')
        password_confirm = getpass.getpass('Confirm password: ')
        
        if password != password_confirm:
            self.stdout.write(self.style.ERROR('Passwords do not match!'))
            return
        
        user.set_password(password)
        user.save()
        
        self.stdout.write(
            self.style.SUCCESS(f'Password reset successfully for {username}!')
        )
    
    def deactivate_user(self, username):
        """Deactivate a user (safer than deletion)"""
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User {username} not found!'))
            return
        
        if user.is_superuser:
            self.stdout.write(self.style.ERROR('Cannot deactivate superuser! This is for security.'))
            return
        
        if not user.is_active:
            self.stdout.write(self.style.WARNING(f'User {username} is already inactive.'))
            return
        
        confirm = input(f'Are you sure you want to deactivate {username}? (y/N): ')
        if confirm.lower() != 'y':
            self.stdout.write('Operation cancelled.')
            return
        
        user.is_active = False
        user.save()
        
        self.stdout.write(
            self.style.SUCCESS(f'User {username} deactivated successfully!')
        )
    
    def activate_user(self, username):
        """Activate a user"""
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User {username} not found!'))
            return
        
        if user.is_active:
            self.stdout.write(self.style.WARNING(f'User {username} is already active.'))
            return
        
        user.is_active = True
        user.save()
        
        self.stdout.write(
            self.style.SUCCESS(f'User {username} activated successfully!')
        )
    
    def backup_users(self):
        """Create a backup of user data"""
        import json
        from datetime import datetime
        
        users_data = []
        for user in User.objects.all():
            users_data.append({
                'username': user.username,
                'email': user.email,
                'is_staff': user.is_staff,
                'is_superuser': user.is_superuser,
                'is_active': user.is_active,
                'date_joined': user.date_joined.isoformat(),
                'last_login': user.last_login.isoformat() if user.last_login else None,
            })
        
        backup_filename = f'user_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        
        with open(backup_filename, 'w') as f:
            json.dump(users_data, f, indent=2)
        
        self.stdout.write(
            self.style.SUCCESS(f'User backup created: {backup_filename}')
        )
