#!/bin/bash

# Make all shell scripts executable for VPS deployment
# Run this script on your VPS after uploading the code

echo "Making shell scripts executable..."

chmod +x deploy_vps.sh
chmod +x build.sh
chmod +x backup_script.sh
chmod +x update_app.sh
chmod +x health_check.sh
chmod +x make_scripts_executable.sh

echo "✅ All scripts are now executable!"
echo ""
echo "You can now run:"
echo "  ./deploy_vps.sh     - Deploy the application"
echo "  ./backup_script.sh  - Create backups"
echo "  ./update_app.sh     - Update the application"
echo "  ./health_check.sh   - Check system health"
