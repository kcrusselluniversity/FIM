import os
import json
import time
import hashlib
from datetime import datetime

CONFIG_FILE = "fim_config.json"
LOG_FILE = "fim_log.txt"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {"files": []}

def log_change(message):
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.now()}: {message}\n")

def calculate_hash(file_path):
    try:
        with open(file_path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    except FileNotFoundError:
        return None

def monitor_files():
    config = load_config()
    file_states = {}

<<<<<<< HEAD
    for entry in config["files"]:
        file_states[entry["path"]] = {
            "hash": calculate_hash(entry["path"]),
        }
=======
    # Function to update file states for new or modified entries in the configuration
    def update_file_states():
        nonlocal config
        config = load_config()  # Reload configuration
        for entry in config["files"]:
            path = entry["path"]
            # If the file is not already being monitored, initialize its state
            if path not in file_states:
                try:
                    file_states[path] = {
                        "hash": calculate_hash(path),      # Compute the current hash of the file
                        "metadata": os.stat(path)         # Get the current metadata of the file
                    }
                except FileNotFoundError:
                    file_states[path] = {
                        "hash": None,                     # File doesn't exist yet
                        "metadata": None
                    }

    # Set up initial state for each monitored file
    update_file_states()
>>>>>>> eec8000 (Refactor code)

    while True:
<<<<<<< HEAD
=======
        # Reload and update file states if configuration has changed
        update_file_states()

        # Iterate over all monitored files in the configuration
>>>>>>> eec8000 (Refactor code)
        for entry in config["files"]:
            path = entry["path"]
            rule = entry["rule"]
            users = entry.get("authorized_users", [])
            
            try:
                current_hash = calculate_hash(path)

                if rule == 1 and os.getlogin() not in users:
                    log_change(f"Unauthorized user modified {path}.")
                elif rule == 2 and (current_hash != file_states[path]["hash"]):
                    log_change(f"File {path} was modified.")
                elif rule == 3:
                    current_hour = datetime.now().hour
                    if (current_hour < 9 or current_hour > 17) and (current_hash != file_states[path]["hash"]):
                        log_change(f"File {path} was modified outside business hours.")
                
                file_states[path] = {
                    "hash": current_hash,
                }
            except FileNotFoundError:
                log_change(f"File {path} was deleted.")

<<<<<<< HEAD
        time.sleep(60)  # Check every minute
=======
        # Wait for 5 seconds before checking the files again
        time.sleep(5)
>>>>>>> eec8000 (Refactor code)

if __name__ == "__main__":
<<<<<<< HEAD
    monitor_files()
=======
    monitor_files()
>>>>>>> eec8000 (Refactor code)
