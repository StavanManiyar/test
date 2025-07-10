#!/bin/bash

# Hostinger VPS Monitoring Script
# Real-time monitoring optimized for 4GB RAM, 1 CPU system

clear
echo "📊 Hostinger VPS Monitoring Dashboard"
echo "======================================"
echo "🎓 Kapadia High School Website"
echo "⏰ $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

# Function to get percentage color
get_color() {
    local percentage=$1
    if [ $percentage -lt 70 ]; then
        echo $GREEN
    elif [ $percentage -lt 85 ]; then
        echo $YELLOW
    else
        echo $RED
    fi
}

# System Information
echo -e "${BLUE}🖥️  SYSTEM INFO${NC}"
echo "════════════════"
echo "Hostname: $(hostname)"
echo "Uptime: $(uptime -p)"
echo "Kernel: $(uname -r)"
echo "OS: $(lsb_release -d | cut -f2)"
echo ""

# CPU Information
echo -e "${BLUE}🖥️  CPU STATUS${NC}"
echo "═══════════════"
cpu_usage=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | awk -F'%' '{print $1}')
cpu_color=$(get_color ${cpu_usage%.*})
echo -e "Usage: ${cpu_color}${cpu_usage}%${NC}"
echo "Load Average: $(uptime | awk -F'load average:' '{print $2}')"
echo "Cores: $(nproc) CPU Core(s)"
echo ""

# Memory Information
echo -e "${BLUE}💾 MEMORY STATUS${NC}"
echo "════════════════"
memory_info=$(free -h | awk 'NR==2{printf "%.0f %.0f %.0f", $3*100/$2, $3, $2}')
read mem_percent mem_used mem_total <<< $memory_info
mem_color=$(get_color $mem_percent)
echo -e "RAM Usage: ${mem_color}${mem_percent}%${NC} ($(free -h | awk 'NR==2{print $3}')GB / $(free -h | awk 'NR==2{print $2}')GB)"
echo "Available: $(free -h | awk 'NR==2{print $7}')GB"
echo "Cached: $(free -h | awk 'NR==2{print $6}')GB"

# Swap Information
swap_info=$(free -h | awk 'NR==3{if($2!="0B") printf "%.0f %s %s", $3*100/$2, $3, $2; else print "0 0B 0B"}')
if [ "$swap_info" != "0 0B 0B" ]; then
    read swap_percent swap_used swap_total <<< $swap_info
    swap_color=$(get_color $swap_percent)
    echo -e "Swap Usage: ${swap_color}${swap_percent}%${NC} (${swap_used} / ${swap_total})"
else
    echo "Swap Usage: 0% (No swap configured)"
fi
echo ""

# Disk Information
echo -e "${BLUE}💿 DISK STATUS${NC}"
echo "══════════════"
disk_info=$(df -h / | awk 'NR==2{printf "%.0f %s %s %s", $5, $3, $2, $4}')
read disk_percent disk_used disk_total disk_available <<< $disk_info
disk_color=$(get_color $disk_percent)
echo -e "Root Usage: ${disk_color}${disk_percent}%${NC} (${disk_used} / ${disk_total})"
echo "Available: ${disk_available}"

# Check other important mount points
echo "Other Disks:"
df -h | grep -E '^/dev/' | grep -v '/$' | while read line; do
    echo "  $line"
done
echo ""

# Docker Container Status
echo -e "${BLUE}🐳 DOCKER STATUS${NC}"
echo "════════════════"
if command -v docker &> /dev/null && docker info &> /dev/null; then
    echo "Docker: ✅ Running"
    
    # Check if docker-compose file exists
    if [ -f "docker-compose.hostinger.yml" ]; then
        echo ""
        echo "Hostinger Containers:"
        docker-compose -f docker-compose.hostinger.yml ps --format "table {{.Name}}\t{{.State}}\t{{.Status}}"
    elif [ -f "docker-compose.yml" ]; then
        echo ""
        echo "Standard Containers:"
        docker-compose ps --format "table {{.Name}}\t{{.State}}\t{{.Status}}"
    fi
    
    echo ""
    echo "Container Resources:"
    docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}" 2>/dev/null || echo "No running containers"
else
    echo "Docker: ❌ Not running or not installed"
fi
echo ""

# Network Status
echo -e "${BLUE}🌐 NETWORK STATUS${NC}"
echo "═════════════════"
if command -v curl &> /dev/null; then
    # Check internet connectivity
    if curl -s --max-time 5 google.com &> /dev/null; then
        echo "Internet: ✅ Connected"
    else
        echo "Internet: ❌ Disconnected"
    fi
    
    # Check website status if domain is configured
    if [ ! -z "$DOMAIN_NAME" ]; then
        website_status=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "https://$DOMAIN_NAME" 2>/dev/null)
        if [ "$website_status" = "200" ]; then
            response_time=$(curl -s -o /dev/null -w "%{time_total}" --max-time 10 "https://$DOMAIN_NAME" 2>/dev/null)
            echo "Website: ✅ Online (${response_time}s response)"
        else
            echo "Website: ❌ Offline or Error (HTTP: $website_status)"
        fi
    fi
else
    echo "Network tools not available"
fi

# Network traffic
if [ -f /proc/net/dev ]; then
    echo "Network Traffic:"
    cat /proc/net/dev | grep -E "(eth0|ens|enp)" | head -1 | awk '{
        rx_mb = $2/1024/1024
        tx_mb = $10/1024/1024
        printf "  RX: %.1f MB | TX: %.1f MB\n", rx_mb, tx_mb
    }'
fi
echo ""

# Security & SSL Status
echo -e "${BLUE}🔒 SECURITY STATUS${NC}"
echo "══════════════════"
if [ -d "ssl" ] && [ -f "ssl/fullchain.pem" ]; then
    ssl_expire=$(openssl x509 -enddate -noout -in ssl/fullchain.pem 2>/dev/null | cut -d= -f2)
    if [ ! -z "$ssl_expire" ]; then
        echo "SSL Certificate: ✅ Valid"
        echo "Expires: $ssl_expire"
    else
        echo "SSL Certificate: ⚠️  Cannot read certificate"
    fi
else
    echo "SSL Certificate: ❌ Not found"
fi

# Check if fail2ban is running
if systemctl is-active --quiet fail2ban 2>/dev/null; then
    echo "Fail2Ban: ✅ Active"
else
    echo "Fail2Ban: ❌ Not active"
fi
echo ""

# Database Status
echo -e "${BLUE}🗄️  DATABASE STATUS${NC}"
echo "═══════════════════"
if docker ps | grep -q postgres; then
    echo "PostgreSQL: ✅ Running"
    
    # Try to get database size if possible
    db_size=$(docker exec $(docker ps -q -f name=db) psql -U postgres -d postgres -t -c "SELECT pg_size_pretty(pg_database_size('postgres'));" 2>/dev/null | xargs)
    if [ ! -z "$db_size" ]; then
        echo "Database Size: $db_size"
    fi
    
    # Check database connections
    db_connections=$(docker exec $(docker ps -q -f name=db) psql -U postgres -d postgres -t -c "SELECT count(*) FROM pg_stat_activity;" 2>/dev/null | xargs)
    if [ ! -z "$db_connections" ]; then
        echo "Active Connections: $db_connections"
    fi
else
    echo "PostgreSQL: ❌ Not running"
fi
echo ""

# Recent Logs
echo -e "${BLUE}📝 RECENT ACTIVITY${NC}"
echo "══════════════════"
echo "System Logs (Last 5):"
journalctl -n 5 --no-pager -q | tail -5

echo ""
echo "Docker Logs (Last 5):"
if [ -f "docker-compose.hostinger.yml" ]; then
    docker-compose -f docker-compose.hostinger.yml logs --tail=5 web 2>/dev/null || echo "No recent docker logs"
elif [ -f "docker-compose.yml" ]; then
    docker-compose logs --tail=5 web 2>/dev/null || echo "No recent docker logs"
else
    echo "No docker-compose file found"
fi
echo ""

# Performance Recommendations
echo -e "${BLUE}💡 PERFORMANCE RECOMMENDATIONS${NC}"
echo "══════════════════════════════"

# CPU recommendations
if [ ${cpu_usage%.*} -gt 80 ]; then
    echo -e "${RED}⚠️  High CPU usage detected (${cpu_usage}%)${NC}"
    echo "   Consider optimizing processes or upgrading VPS"
fi

# Memory recommendations
if [ $mem_percent -gt 85 ]; then
    echo -e "${RED}⚠️  High memory usage detected (${mem_percent}%)${NC}"
    echo "   Consider restarting containers or upgrading RAM"
elif [ $mem_percent -gt 70 ]; then
    echo -e "${YELLOW}⚠️  Moderate memory usage (${mem_percent}%)${NC}"
    echo "   Monitor closely and consider optimization"
fi

# Disk recommendations
if [ $disk_percent -gt 85 ]; then
    echo -e "${RED}⚠️  High disk usage detected (${disk_percent}%)${NC}"
    echo "   Consider cleaning logs or upgrading storage"
elif [ $disk_percent -gt 70 ]; then
    echo -e "${YELLOW}⚠️  Moderate disk usage (${disk_percent}%)${NC}"
    echo "   Regular cleanup recommended"
fi

echo ""
echo -e "${GREEN}📊 Monitoring completed at $(date '+%H:%M:%S')${NC}"
echo -e "${CYAN}💡 Run './monitor_hostinger.sh' anytime to check status${NC}"
echo ""
