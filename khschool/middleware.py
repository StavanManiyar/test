from django.http import HttpResponseForbidden
from django.core.cache import cache
from django.conf import settings
from django.contrib.auth.models import User
import logging
import os
import time

logger = logging.getLogger(__name__)

class AdminSecurityMiddleware:
    """
    Custom middleware to secure admin panel access
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        # Get admin URL from environment or use default
        self.admin_url = os.environ.get('ADMIN_URL', 'khs-secure-admin-2024/')
        if not self.admin_url.endswith('/'):
            self.admin_url += '/'
        
        # Allowed IP addresses for admin access (configure these for your VPS)
        self.allowed_ips = [
            '127.0.0.1',
            '::1',
            'localhost',
        ]
        
        # Add VPS IP if available
        vps_ip = os.environ.get('VPS_SERVER_IP')
        if vps_ip:
            self.allowed_ips.append(vps_ip)
        
        # Rate limiting settings
        self.max_attempts = 5  # Max login attempts
        self.block_duration = 900  # 15 minutes in seconds
        
    def __call__(self, request):
        # Check if request is for admin panel
        if request.path.startswith(f'/{self.admin_url}'):
            # Security checks
            if not self.check_ip_allowed(request):
                logger.warning(f"Admin access denied for IP: {self.get_client_ip(request)}")
                return HttpResponseForbidden("Access denied: IP not allowed")
            
            if not self.check_rate_limit(request):
                logger.warning(f"Rate limit exceeded for IP: {self.get_client_ip(request)}")
                return HttpResponseForbidden("Access denied: Too many attempts")
            
            # Log admin access
            if request.user.is_authenticated:
                logger.info(f"Admin access by {request.user.username} from {self.get_client_ip(request)}")
        
        response = self.get_response(request)
        
        # Track failed login attempts
        if (request.path.startswith(f'/{self.admin_url}') and 
            request.method == 'POST' and 
            'username' in request.POST and 
            not request.user.is_authenticated):
            self.record_failed_attempt(request)
        
        return response
    
    def get_client_ip(self, request):
        """Get client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def check_ip_allowed(self, request):
        """Check if IP is allowed to access admin"""
        client_ip = self.get_client_ip(request)
        
        # Allow all IPs in DEBUG mode
        if settings.DEBUG:
            return True
            
        # Check against allowed IPs
        return client_ip in self.allowed_ips
    
    def check_rate_limit(self, request):
        """Check rate limiting for admin access"""
        client_ip = self.get_client_ip(request)
        cache_key = f"admin_attempts_{client_ip}"
        
        attempts = cache.get(cache_key, 0)
        
        if attempts >= self.max_attempts:
            # Check if block time has expired
            block_key = f"admin_blocked_{client_ip}"
            block_time = cache.get(block_key)
            
            if block_time and (time.time() - block_time) < self.block_duration:
                return False
            else:
                # Reset attempts after block period
                cache.delete(cache_key)
                cache.delete(block_key)
        
        return True
    
    def record_failed_attempt(self, request):
        """Record failed login attempt"""
        client_ip = self.get_client_ip(request)
        cache_key = f"admin_attempts_{client_ip}"
        
        attempts = cache.get(cache_key, 0) + 1
        cache.set(cache_key, attempts, self.block_duration)
        
        if attempts >= self.max_attempts:
            # Block the IP
            block_key = f"admin_blocked_{client_ip}"
            cache.set(block_key, time.time(), self.block_duration)
            
            logger.warning(f"IP {client_ip} blocked for {self.block_duration} seconds after {attempts} failed attempts")
        
        logger.warning(f"Failed admin login attempt from {client_ip} (attempt {attempts})")
