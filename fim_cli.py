import argparse
import json
import os

# File name for storing configuration data
CONFIG_FILE = "fim_config.json"

# Load configuration from the JSON file or initialize an empty config
def load_config():
    if os.path.exists(CONFIG_FILE):  
        with open(CONFIG_FILE, "r") as f: 
            return json.load(f)  
    return {"files": []}

# Save the updated configuration back to the JSON file
def save_config(config):
    with open(CONFIG_FILE, "w") as f:  
        json.dump(config, f, indent=4) 

# Add a file to the list of monitored files
def add_file(file_path, rule, authorized_users=None):
    config = load_config()  
    for entry in config["files"]:  
        if entry["path"] == file_path:
            print("File already monitored.")  
            return
    entry = {"path": file_path, "rule": rule}  
    if rule == 1:  
        entry["authorized_users"] = authorized_users or []
    config["files"].append(entry)  
    save_config(config)  
    print("File added for monitoring.")  

# Remove a file from the list of monitored files
def remove_file(file_path):
    config = load_config() 
    # Filter out the file to be removed from the list of monitored files
    config["files"] = [f for f in config["files"] if f["path"] != file_path]
    save_config(config) 
    print("File removed from monitoring.") 

# Display all files currently being monitored
def view_files():
    config = load_config() 
    if not config["files"]:  
        print("No files are currently being monitored.") 
    else:
        for entry in config["files"]:  
            print(entry)  

# Print the monitoring log file
def print_log():
    if os.path.exists("fim_log.txt"):  
        with open("fim_log.txt", "r") as f: 
            print(f.read())  
    else:
        print("No logs available.") 

# Main function to handle CLI commands
if __name__ == "__main__":
    # Create a CLI parser
    parser = argparse.ArgumentParser(description="File Integrity Monitor CLI")  
    subparsers = parser.add_subparsers(dest="command")  

    # Subparser for the "add" command
    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("absolute_file_path", help="Absolute path to the file to monitor")
    add_parser.add_argument("rule", type=int, help='''Rule to apply (1: Only authorised users can change the file, 2: 
    No changes can be made to the file, 3: Changes to the file only allowed during business hours)''')
    add_parser.add_argument("--users", nargs="*", help="Authorized users (for Rule 1)")

    # Subparser for the "remove" command
    remove_parser = subparsers.add_parser("remove")
    remove_parser.add_argument("absolute_file_path", help="Absolute path to the file to remove from monitoring")

    # Subparser for the "view" command
    view_parser = subparsers.add_parser("view", help="View monitored files")

    # Subparser for the "log" command
    log_parser = subparsers.add_parser("log", help="Print the monitoring log")

    args = parser.parse_args()  # Parse the provided command-line arguments

    # Handle each command based on user input
    if args.command == "add":
        add_file(args.absolute_file_path, args.rule, args.users)  
    elif args.command == "remove":
        remove_file(args.absolute_file_path)  
    elif args.command == "view":
        view_files()  
    elif args.command == "log":
        print_log()
    else:
        # Print help message if command is not recognized
        parser.print_help() 
