#!/bin/bash

# Hostinger VPS Optimization Script
# Optimizes system for 4GB RAM, 1 CPU Core, 50GB NVMe SSD

echo "🔧 Optimizing Hostinger VPS for best performance..."

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Memory Optimizations for 4GB RAM
echo -e "${BLUE}💾 Optimizing memory settings...${NC}"
cat >> /etc/sysctl.conf << 'EOF'
# Hostinger VPS Memory Optimizations (4GB RAM)
vm.swappiness=10
vm.dirty_ratio=15
vm.dirty_background_ratio=5
vm.vfs_cache_pressure=50
vm.min_free_kbytes=65536

# Network Optimizations
net.core.rmem_max = 16777216
net.core.wmem_max = 16777216
net.ipv4.tcp_rmem = 4096 12582912 16777216
net.ipv4.tcp_wmem = 4096 12582912 16777216
net.ipv4.tcp_congestion_control = bbr
net.core.netdev_max_backlog = 5000

# File System Optimizations
fs.file-max = 65536
EOF

# Apply settings immediately
sysctl -p

# Docker Optimizations for Single Core
echo -e "${BLUE}🐳 Optimizing Docker for single core...${NC}"
mkdir -p /etc/docker
cat > /etc/docker/daemon.json << 'EOF'
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  },
  "default-ulimits": {
    "nofile": {
      "Name": "nofile",
      "Hard": 64000,
      "Soft": 64000
    }
  },
  "storage-driver": "overlay2",
  "storage-opts": [
    "overlay2.override_kernel_check=true"
  ]
}
EOF

# PostgreSQL Configuration for 4GB RAM
echo -e "${BLUE}🗄️ Creating optimized PostgreSQL config...${NC}"
cat > postgresql.hostinger.conf << 'EOF'
# PostgreSQL Configuration optimized for Hostinger VPS (4GB RAM, 1 CPU)

# Memory Settings
shared_buffers = 1GB                    # 25% of RAM
effective_cache_size = 3GB              # 75% of RAM
work_mem = 4MB                          # Conservative for single core
maintenance_work_mem = 256MB            # For maintenance operations

# Checkpoint Settings
checkpoint_completion_target = 0.9
wal_buffers = 16MB
min_wal_size = 1GB
max_wal_size = 4GB

# Performance Settings
random_page_cost = 1.1                  # NVMe SSD optimized
effective_io_concurrency = 200          # SSD concurrent I/O
default_statistics_target = 100

# Connection Settings
max_connections = 100                   # Conservative for 4GB RAM
shared_preload_libraries = 'pg_stat_statements'

# Worker Processes (Single Core Optimization)
max_worker_processes = 2
max_parallel_workers_per_gather = 1
max_parallel_workers = 2
max_parallel_maintenance_workers = 1

# Logging (Reduced for performance)
log_statement = 'none'
log_duration = off
log_lock_waits = on
log_temp_files = 10MB
EOF

# Nginx Optimization for Single Core
echo -e "${BLUE}🌐 Creating optimized Nginx worker config...${NC}"
cat > nginx.worker.conf << 'EOF'
# Nginx worker optimization for Hostinger VPS (1 CPU)
worker_processes 1;
worker_cpu_affinity 1;
worker_rlimit_nofile 65535;

events {
    worker_connections 1024;
    use epoll;
    multi_accept on;
}
EOF

# Disk I/O Optimizations for NVMe SSD
echo -e "${BLUE}💿 Optimizing disk I/O for NVMe SSD...${NC}"
cat >> /etc/fstab << 'EOF'
# NVMe SSD optimizations
tmpfs /tmp tmpfs defaults,noatime,nosuid,nodev,noexec,mode=1777,size=512M 0 0
EOF

# Create swap file (1GB for 4GB RAM system)
echo -e "${BLUE}🔄 Setting up optimized swap...${NC}"
if [ ! -f /swapfile ]; then
    fallocate -l 1G /swapfile
    chmod 600 /swapfile
    mkswap /swapfile
    swapon /swapfile
    echo '/swapfile none swap sw 0 0' >> /etc/fstab
fi

# System limits optimization
echo -e "${BLUE}⚙️ Optimizing system limits...${NC}"
cat >> /etc/security/limits.conf << 'EOF'
# Hostinger VPS optimized limits
* soft nofile 65536
* hard nofile 65536
* soft nproc 32768
* hard nproc 32768
root soft nofile 65536
root hard nofile 65536
EOF

# Logrotate optimization
echo -e "${BLUE}📝 Setting up log rotation...${NC}"
cat > /etc/logrotate.d/hostinger-optimization << 'EOF'
/var/log/nginx/*.log {
    daily
    missingok
    rotate 7
    compress
    delaycompress
    notifempty
    create 0644 www-data adm
    sharedscripts
    postrotate
        if [ -f /var/run/nginx.pid ]; then
            nginx -s reload > /dev/null 2>&1
        fi
    endscript
}

/var/lib/docker/containers/*/*.log {
    rotate 7
    daily
    compress
    size=1M
    missingok
    delaycompress
    copytruncate
}
EOF

# Create monitoring script
echo -e "${BLUE}📊 Creating system monitoring script...${NC}"
cat > /usr/local/bin/hostinger-monitor << 'EOF'
#!/bin/bash
echo "📊 Hostinger VPS Status - $(date)"
echo "=================================="
echo "🖥️  CPU: $(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | awk -F'%' '{print $1"%"}')"
echo "💾 RAM: $(free -h | awk 'NR==2{printf "%.1f%% (%s/%s)\n", $3*100/$2, $3, $2}')"
echo "💿 Disk: $(df -h / | awk 'NR==2{printf "%s (%s used)\n", $5, $3}')"
echo "🌡️  Load: $(uptime | awk -F'load average:' '{print $2}')"
echo "🔄 Swap: $(free -h | awk 'NR==3{printf "%s/%s (%.1f%%)\n", $3, $2, $3*100/$2}')"
echo "🌐 Network: $(cat /proc/net/dev | grep eth0 | awk '{printf "RX: %sMB TX: %sMB\n", $2/1024/1024, $10/1024/1024}')"
EOF

chmod +x /usr/local/bin/hostinger-monitor

# Restart Docker if it was running
if systemctl is-active --quiet docker; then
    echo -e "${YELLOW}🔄 Restarting Docker with new configuration...${NC}"
    systemctl restart docker
fi

echo -e "${GREEN}✅ Hostinger VPS optimization completed!${NC}"
echo ""
echo -e "${BLUE}📊 Monitor your VPS with: hostinger-monitor${NC}"
echo -e "${BLUE}🔧 Applied optimizations:${NC}"
echo "  • Memory management for 4GB RAM"
echo "  • Single-core CPU optimization"
echo "  • NVMe SSD I/O tuning"
echo "  • Docker container limits"
echo "  • PostgreSQL performance tuning"
echo "  • Nginx worker optimization"
echo "  • Log rotation and cleanup"
echo "  • System resource limits"
echo ""
echo -e "${GREEN}🚀 Your Hostinger VPS is now optimized for maximum performance!${NC}"
