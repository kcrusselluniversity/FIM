#!/bin/bash

# Bash script to set up the FIM project

# Function to print messages in color
print_message() {
    echo -e "\033[1;32m$1\033[0m"
}

print_message "Starting FIM setup..."

# Prompt the user about Elasticsearch configuration
print_message "Do you want to configure Elasticsearch now? (Y/N)"
read -r use_elasticsearch

# Create .env file with either a real API key or a placeholder
ENV_FILE=".env"
if [ "$use_elasticsearch" == "Y" ] || [ "$use_elasticsearch" == "y" ]; then
    print_message "Please enter your Elasticsearch API key:"
    read -r api_key
    echo "API_KEY=$api_key" > "$ENV_FILE"
    print_message ".env file created with your API key."
else
    echo "API_KEY=your_elasticsearch_api_key_here" > "$ENV_FILE"
    print_message ".env file created with a placeholder API key. You can configure it later."
fi
sleep 3

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
sleep 3

# Reload systemd to register the service
print_message "Reloading systemd daemon to apply changes..."
sudo systemctl daemon-reload

# Enable and start the fim_monitor service
print_message "Enabling and starting fim_monitor service..."
sudo systemctl enable fim_monitor
sudo systemctl start fim_monitor
sleep 2

# Final message
print_message "Setup complete!"
sleep 2
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