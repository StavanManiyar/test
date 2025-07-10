"""
URL configuration for kapadiaschool project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
import os

# Generate a secure admin URL from environment variable or use a default secure one
ADMIN_URL = os.environ.get('ADMIN_URL', 'khs-secure-admin-2024/')

# Build URL patterns based on whether ADMIN_URL is different from 'admin/'
urlpatterns = []

# Add the admin URL (either secure or standard, but not both)
urlpatterns.append(path(ADMIN_URL, admin.site.urls))

# Add the main app URLs
urlpatterns.append(path('', include('khschool.urls')))

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

#admin portal text
admin.site.site_header = "Kapadia High School"
admin.site.site_title = " Kapadia High School Admin Portal"
admin.site.index_title = "Welcome to Kapadia High School Portal"