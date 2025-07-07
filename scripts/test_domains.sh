#!/bin/bash

# Domain Testing Script for Kapadia High School
# This script tests all domain variations to ensure proper redirects

echo "🌐 Testing Domain Configuration for Kapadia High School..."
echo "=================================================="

# Test domains
DOMAIN="kapadiahighschool.com"
WWW_DOMAIN="www.kapadiahighschool.com"

# Function to test HTTP response
test_url() {
    local url=$1
    local expected_description=$2
    
    echo "Testing: $url"
    
    # Get response code and final URL
    response=$(curl -s -o /dev/null -w "%{http_code}|%{url_effective}" -L "$url" 2>/dev/null || echo "000|ERROR")
    http_code=$(echo $response | cut -d'|' -f1)
    final_url=$(echo $response | cut -d'|' -f2)
    
    echo "  Response Code: $http_code"
    echo "  Final URL: $final_url"
    echo "  Expected: $expected_description"
    
    case $http_code in
        200)
            echo "  Status: ✅ Success"
            ;;
        301|302)
            echo "  Status: ✅ Redirect (as expected)"
            ;;
        000)
            echo "  Status: ❌ Connection failed"
            ;;
        *)
            echo "  Status: ⚠️  Unexpected response code"
            ;;
    esac
    echo ""
}

# Function to check DNS resolution
check_dns() {
    local domain=$1
    echo "🔍 Checking DNS for $domain"
    
    # Check if nslookup is available
    if command -v nslookup >/dev/null 2>&1; then
        result=$(nslookup $domain 2>/dev/null | grep "Address:" | tail -1 | awk '{print $2}')
        if [ -n "$result" ] && [ "$result" != "127.0.0.1" ]; then
            echo "  DNS Resolution: ✅ $result"
        else
            echo "  DNS Resolution: ❌ Not resolved or localhost"
        fi
    else
        echo "  DNS Resolution: ⚠️  nslookup not available"
    fi
    echo ""
}

echo "📋 DNS Resolution Check"
echo "----------------------"
check_dns $DOMAIN
check_dns $WWW_DOMAIN

echo "🌐 HTTP/HTTPS Testing"
echo "--------------------"

# Test all combinations
test_url "http://$DOMAIN" "Should redirect to HTTPS"
test_url "https://$DOMAIN" "Should load successfully"
test_url "http://$WWW_DOMAIN" "Should redirect to HTTPS non-www"
test_url "https://$WWW_DOMAIN" "Should redirect to HTTPS non-www"

echo "🔒 SSL Certificate Check"
echo "-----------------------"

# Check SSL certificate
if command -v openssl >/dev/null 2>&1; then
    echo "Checking SSL certificate for $DOMAIN..."
    
    # Get certificate info
    cert_info=$(echo | openssl s_client -servername $DOMAIN -connect $DOMAIN:443 2>/dev/null | openssl x509 -noout -dates 2>/dev/null)
    
    if [ $? -eq 0 ] && [ -n "$cert_info" ]; then
        echo "  SSL Certificate: ✅ Valid"
        
        # Extract expiry date
        expiry=$(echo "$cert_info" | grep "notAfter" | cut -d= -f2)
        if [ -n "$expiry" ]; then
            expiry_timestamp=$(date -d "$expiry" +%s 2>/dev/null || echo "0")
            current_timestamp=$(date +%s)
            days_until_expiry=$(( (expiry_timestamp - current_timestamp) / 86400 ))
            
            if [ $days_until_expiry -gt 0 ]; then
                echo "  Expires in: $days_until_expiry days"
                if [ $days_until_expiry -lt 30 ]; then
                    echo "  Status: ⚠️  Certificate expires soon!"
                else
                    echo "  Status: ✅ Certificate is valid"
                fi
            else
                echo "  Status: ❌ Certificate expired or invalid date"
            fi
        fi
    else
        echo "  SSL Certificate: ❌ Not available or invalid"
    fi
else
    echo "  SSL Check: ⚠️  OpenSSL not available"
fi

echo ""
echo "🎯 Admin Panel Test"
echo "------------------"
test_url "https://$DOMAIN/admin/" "Should load Django admin login"

echo "📊 Summary"
echo "=========="
echo "Your domain configuration should work as follows:"
echo ""
echo "✅ Main URL: https://$DOMAIN"
echo "✅ Alternative: https://$WWW_DOMAIN (redirects to main)"
echo "✅ HTTP redirects: All HTTP URLs redirect to HTTPS"
echo "✅ Admin panel: https://$DOMAIN/admin/"
echo ""
echo "If any tests failed:"
echo "1. Check DNS propagation (can take up to 48 hours)"
echo "2. Verify VPS is running: ./health_check.sh"
echo "3. Check Nginx configuration: sudo nginx -t"
echo "4. Review SSL setup if certificate issues"
echo ""
echo "For troubleshooting, see VPS.md and MAINTENANCE_GUIDE.md"
