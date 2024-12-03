import os
import json
import time
import hashlib
from datetime import datetime
from elasticsearch import Elasticsearch
from decouple import config

# Configuration files
CONFIG_FILE = "fim_config.json"
LOG_FILE = "fim_log.txt"

# Elasticsearch configuration
ELASTICSEARCH_HOST = "https://10.0.0.5:9200"  # Update with your Elasticsearch host
CA_CERT_PATH = "/etc/elasticsearch/certs/http_ca.crt"
API_KEY = config("API_KEY") # Import API KEY value from .env file
ELASTICSEARCH_INDEX = "fim_logs"  # Index name for storing logs

# Initialize Elasticsearch client
es = Elasticsearch(
    ELASTICSEARCH_HOST,
    ca_certs=CA_CERT_PATH,
    api_key=API_KEY,
)

# Load configuration
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {"files": []}

# Log changes locally and send to Elasticsearch
def log_change(message, file_path, rule, user=None):
    timestamp = datetime.now()
    log_entry = {
        "timestamp": timestamp.isoformat(),
        "message": message,
        "file_path": file_path,
        "rule": rule,
        "user": user,
    }
    # Write log to local file
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

    # Send log entry to Elasticsearch
    try:
        es.index(index=ELASTICSEARCH_INDEX, document=log_entry)
    except Exception as e:
        print(f"Failed to send log to Elasticsearch: {e}")

# Calculate file hash
def calculate_hash(file_path):
    try:
        with open(file_path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    except FileNotFoundError:
        return None

# Monitor files for changes
def monitor_files():
    config = load_config()
    file_states = {}

    # Update file states for new or modified entries
    def update_file_states():
        nonlocal config
        config = load_config()
        for entry in config["files"]:
            path = entry["path"]
            if path not in file_states:
                try:
                    file_states[path] = {
                        "hash": calculate_hash(path),
                        "metadata": os.stat(path),
                    }
                except FileNotFoundError:
                    file_states[path] = {"hash": None, "metadata": None}

    # Initial file state setup
    update_file_states()

    while True:
        update_file_states()

        for entry in config["files"]:
            path = entry["path"]
            rule = entry["rule"]
            users = entry.get("authorized_users", [])

            try:
                current_hash = calculate_hash(path)

                if rule == 1 and os.getlogin() not in users:
                    log_change(
                        f"Unauthorized user modified {path}.",
                        path,
                        rule,
                        os.getlogin(),
                    )
                elif rule == 2 and current_hash != file_states[path]["hash"]:
                    log_change(f"File {path} was modified.", path, rule)
                elif rule == 3:
                    current_hour = datetime.now().hour
                    if (current_hour < 9 or current_hour > 17) and current_hash != file_states[path]["hash"]:
                        log_change(
                            f"File {path} was modified outside business hours.",
                            path,
                            rule,
                        )

                file_states[path] = {"hash": current_hash}
            except FileNotFoundError:
                log_change(f"File {path} was deleted.", path, None)

        time.sleep(5)

if __name__ == "__main__":
    monitor_files()
