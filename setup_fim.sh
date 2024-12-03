#!/bin/bash

# Bash script to set up the FIM project

# Function to print messages in color
print_message() {
    echo -e "\033[1;32m$1\033[0m"
}

print_message "Starting FIM setup..."

# Update and install necessary packages
print_message "Updating package list and installing Python and pip..."
sudo apt update && sudo apt install -y python3 python3-pip

# Install Python dependencies
print_message "Installing required Python packages..."
sudo apt install python3-elasticsearch
sudo apt install python3-decouple

# Create a systemd service file for fim_monitor
SERVICE_FILE="/etc/systemd/system/fim_monitor.service"
print_message "Creating systemd service for fim_monitor..."
sudo bash -c "cat > $SERVICE_FILE" <<EOL
[Unit]
Description=File Integrity Monitor Background Service
After=network.target

[Service]
ExecStart=$(which python3) $(pwd)/fim_monitor.py
WorkingDirectory=$(pwd)
Restart=always
User=$(whoami)

[Install]
WantedBy=multi-user.target
EOL

# Reload systemd to register the service
print_message "Reloading systemd daemon to apply changes..."
sudo systemctl daemon-reload

# Enable and start the fim_monitor service
print_message "Enabling and starting fim_monitor service..."
sudo systemctl enable fim_monitor
sudo systemctl start fim_monitor

# Create .env file for Elasticsearch API key (if needed)
ENV_FILE=".env"
if [ ! -f "$ENV_FILE" ]; then
    print_message "Creating .env file for Elasticsearch API key..."
    echo "API_KEY=your_elasticsearch_api_key_here" > "$ENV_FILE"
    print_message "Replace 'your_elasticsearch_api_key_here' with your actual API key in the .env file."
fi

# Final message
print_message "Setup complete!"
print_message "How to use FIM CLI:"
echo "1. Add a file to monitor:"
echo "   python3 fim_cli.py add <absolute_file_path> <rule_number> [--users <user1> <user2> ...]"
echo ""
echo "2. Remove a file from monitoring:"
echo "   python3 fim_cli.py remove <absolute_file_path>"
echo ""
echo "3. View monitored files:"
echo "   python3 fim_cli.py view"
echo ""
echo "4. Print the monitoring log:"
echo "   python3 fim_cli.py log"
echo ""
print_message "The FIM monitor service is running in the background. Logs are stored locally and sent to Elasticsearch."