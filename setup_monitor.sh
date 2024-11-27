#!/bin/bash

# Setup FIM monitoring script to run at startup
SERVICE_FILE="/etc/systemd/system/fim_monitor.service"

echo "[Unit]
Description=File Integrity Monitor

[Service]
ExecStart=$(pwd)/fim_monitor.py
Restart=on-failure

[Install]
WantedBy=multi-user.target" > $SERVICE_FILE

chmod +x fim_monitor.py
systemctl enable fim_monitor.service
systemctl start fim_monitor.service

echo "File Integrity Monitor has been set up to run at startup."