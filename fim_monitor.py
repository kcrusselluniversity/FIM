import os
import json
import time
import hashlib
from datetime import datetime

# File paths for the configuration file and log file
CONFIG_FILE = "fim_config.json"  # Configuration file storing monitored files and rules
LOG_FILE = "fim_log.txt"         # Log file for recording changes to monitored files

# Load the configuration file, returning the file monitoring settings
def load_config():
    # Check if the configuration file exists
    if os.path.exists(CONFIG_FILE):
        # Open and load the JSON content of the configuration file
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    # Return a default configuration if the file doesn't exist
    return {"files": []}

# Append a message to the log file with a timestamp
def log_change(message):
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.now()}: {message}\n")

# Calculate the hash (SHA-256) of a file's contents
def calculate_hash(file_path):
    try:
        with open(file_path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    except FileNotFoundError:
        return None

# Main function to monitor the files for changes based on defined rules
def monitor_files():
    # Load the configuration data from the configuration file
    config = load_config()
    # Initialize a dictionary to store the state of each monitored file (hash and metadata)
    file_states = {}

    # Set up initial state for each monitored file
    for entry in config["files"]:
        file_states[entry["path"]] = {
            "hash": calculate_hash(entry["path"]),       # Compute the current hash of the file
            "metadata": os.stat(entry["path"])           # Get the current metadata of the file
        }

    # Infinite loop to continuously monitor files
    while True:
        # Iterate over all monitored files in the configuration
        for entry in config["files"]:
            path = entry["path"]                        # Get the file path
            rule = entry["rule"]                        # Get the monitoring rule for this file
            users = entry.get("authorized_users", [])   # Get the list of authorized users (for Rule 1)

            try:
                # Get the current hash of the file
                current_hash = calculate_hash(path)

                # Rule 1: Only authorized users can modify the file
                if rule == 1 and os.getlogin() not in users:
                    log_change(f"Unauthorized user ({os.getlogin()}) modified {path}.")
                
                # Rule 2: No changes are allowed to the file
                elif rule == 2 and (current_hash != file_states[path]["hash"]):
                    log_change(f"File {path} was modified.")
                
                # Rule 3: Changes are allowed only during business hours (9 AM to 5 PM)
                elif rule == 3:
                    current_hour = datetime.now().hour   # Get the current hour
                    # Log a change if it happens outside business hours and the file hash has changed
                    if (current_hour < 9 or current_hour > 17) and (current_hash != file_states[path]["hash"]):
                        log_change(f"File {path} was modified outside business hours.")
                
                # Update the stored state for this file (hash and metadata)
                file_states[path] = {
                    "hash": current_hash,
                }
            except FileNotFoundError:
                # Log if the file is deleted or missing
                log_change(f"File {path} was deleted.")

        # Wait for 60 seconds before checking the files again
        time.sleep(60)

# Entry point for the script
if __name__ == "__main__":
    monitor_files() 
