#!/bin/bash

# Variables
MONITOR_SCRIPT="fim_monitor.py"
SERVICE_FILE="/etc/systemd/system/fim_monitor.service"
WORKING_DIR=$(pwd)
PYTHON_PATH=$(which python3)

# Check if the monitoring script exists
if [ ! -f "$WORKING_DIR/$MONITOR_SCRIPT" ]; then
    echo "[ERROR] Monitoring script '$MONITOR_SCRIPT' not found in $WORKING_DIR."
    echo "Make sure the script is in the current directory and try again."
    exit 1
fi

# Create the systemd service file
echo "Creating systemd service file..."
sudo bash -c "cat > $SERVICE_FILE" <<EOL
[Unit]
Description=File Integrity Monitor Daemon
After=network.target

[Service]
ExecStart=$PYTHON_PATH $WORKING_DIR/$MONITOR_SCRIPT
WorkingDirectory=$WORKING_DIR
Restart=always
User=$(whoami)
Group=$(id -gn)

[Install]
WantedBy=multi-user.target
EOL

if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to create systemd service file."
    exit 1
fi

# Reload systemd daemon
echo "Reloading systemd daemon..."
sudo systemctl daemon-reload

# Enable and start the service
echo "Enabling and starting the File Integrity Monitor service..."
sudo systemctl enable fim_monitor.service
sudo systemctl start fim_monitor.service

# Check service status
sudo systemctl status fim_monitor.service --no-pager

echo "Setup complete! The File Integrity Monitor is now running as a background service."
echo "You can use the 'fim_cli.py' script to manage monitored files."
