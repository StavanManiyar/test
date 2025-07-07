# 🔧 Deployment and Maintenance Scripts

## 🚀 Deployment Scripts

- **`deploy.sh`** - Main VPS deployment script
- **`deploy_vps.sh`** - Alternative VPS deployment
- **`build.sh`** - Build process for production

## 🔧 Maintenance Scripts

- **`backup_script.sh`** - Database backup automation
- **`health_check.sh`** - System health monitoring
- **`update_app.sh`** - Application update process
- **`setup_cron.sh`** - Setup scheduled tasks

## 🧪 Testing Scripts

- **`test_domains.sh`** - Domain connectivity testing
- **`make_scripts_executable.sh`** - Make all scripts executable

## 📋 Usage

```bash
# Make scripts executable
chmod +x scripts/*.sh

# Deploy to VPS
./scripts/deploy.sh

# Check system health
./scripts/health_check.sh

# Backup database
./scripts/backup_script.sh
```

## ⚠️ Important Notes

1. **Update VPS details** in deploy.sh before running
2. **Test locally** before deploying to production
3. **Backup database** before major updates
