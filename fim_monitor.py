#!/usr/bin/env python3

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

    for entry in config["files"]:
        file_states[entry["path"]] = {
            "hash": calculate_hash(entry["path"]),
            "metadata": os.stat(entry["path"])
        }

    while True:
        for entry in config["files"]:
            path = entry["path"]
            rule = entry["rule"]
            users = entry.get("authorized_users", [])
            
            try:
                current_hash = calculate_hash(path)
                current_metadata = os.stat(path)

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
                    "metadata": current_metadata
                }
            except FileNotFoundError:
                log_change(f"File {path} was deleted.")

        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    monitor_files()